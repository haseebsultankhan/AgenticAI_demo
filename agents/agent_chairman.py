# agents/agent_chairman.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "chairman.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# SYNC RESPONSE (fallback)
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions about the current Chairman and leadership engagement. "
                "Only use the provided official context. Do not generate speculative responses or assume responsibilities."

                "\n\nExamples:\n"
                "Q: Who is the Chairman of NADRA?\n"
                "A: Lieutenant General Muhammad Munir Afsar is the current Chairman of NADRA.\n\n"
                "Q: When did chairman appointed?\n"
                "A: Lieutenant General Muhammad Munir Afsar is serving as the Chairman of NADRA since 2nd October 2023\n\n" 
                "Q: Can I speak with the chairman?\n"
                "A: The chairman hosts regular Khuli Kachehri sessions to engage with the public.\n\n"
                "Q: Where can I find chairman's message?\n"
                "A: Visit: https://www.nadra.gov.pk/chairman-nadra\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "chairman.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# ASYNC STREAMING (FastAPI StreamingResponse)
# ────────────────────────────────────────────────────────────────────────────────
async def handle_query_stream(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions about the current Chairman and leadership engagement. "
                "Only use the provided official context. Do not generate speculative responses or assume responsibilities."

                "\n\nExamples:\n"
                "Q: Who is the Chairman of NADRA?\n"
                "A: Lieutenant General Muhammad Munir Afsar is the current Chairman of NADRA.\n\n"
                "Q: When was chairman appointed?\n"
                "A: Lieutenant General Muhammad Munir Afsar is serving as the Chairman of NADRA since 2nd October 2023\n\n" 
                "Q: Can I speak with the chairman?\n"
                "A: The chairman hosts regular Khuli Kachehri sessions to engage with the public.\n\n"
                "Q: Where can I find chairman's message?\n"
                "A: Visit: https://www.nadra.gov.pk/chairman-nadra\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk

