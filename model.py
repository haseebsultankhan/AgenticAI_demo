# model.py

import ollama
import numpy as np
import asyncio
from ollama import AsyncClient

# Model identifiers
LLM_MODEL = "granite3.3:latest"
EMBED_MODEL = "bge-m3"

# Limit concurrent GPU model usage (2 is safe for 3090, can tune later)
llm_semaphore = asyncio.Semaphore(50)

# ────────────────────────────────────────────────────────────────────────────────
# SYNC RESPONSE (used by agents like location, documents, etc.)
# ────────────────────────────────────────────────────────────────────────────────
def get_llm_response(messages, model=LLM_MODEL):
    """
    Accepts a list of messages (chat format) and returns LLM response.
    Example: [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    """
    response = ollama.chat(model=model, messages=messages)
    return response["message"]["content"].strip()

# ────────────────────────────────────────────────────────────────────────────────
# STREAMING RESPONSE (async, supports partial tokens via yield)
# ────────────────────────────────────────────────────────────────────────────────
async def stream_llm_response(messages, model=LLM_MODEL):
    """
    Streams response content from Ollama LLM using async + generator.
    Use in FastAPI's StreamingResponse.
    """
    # message = {"role": "user", "content": prompt}
    async with llm_semaphore:  # prevent GPU overload
        client = AsyncClient()
        async for part in await client.chat(model=model, messages=messages, stream=True):
            yield part["message"]["content"]

# ────────────────────────────────────────────────────────────────────────────────
# EMBEDDING RESPONSE
# ────────────────────────────────────────────────────────────────────────────────
def get_embedding(text, model=EMBED_MODEL):
    """
    Returns 1024-dim float32 vector from bge-m3 via Ollama.
    """
    response = ollama.embeddings(model=model, prompt=text)
    if "embedding" in response:
        return np.array(response["embedding"], dtype=np.float32)
    elif "embeddings" in response:
        return np.array(response["embeddings"][0], dtype=np.float32)
    else:
        raise RuntimeError("No embedding returned from Ollama.")
