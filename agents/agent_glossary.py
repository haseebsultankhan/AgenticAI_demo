# agents/agent_glossary.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# LOAD GLOSSARY CONTEXT
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "glossary_final.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# SYNC RESPONSE
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a glossary assistant. Define NADRA-related terms like CNIC, NICOP, POC, FRC, Smart CNIC, etc. using only the official definitions from the document."
                "Do not make up definitions or add examples unless clearly present."

                "\n\nExamples:\n"
                "Q: What is NICOP?\n"
                "A: NICOP is the National Identity Card for Overseas Pakistanis, issued to eligible citizens living abroad.\n\n"
                "Q: What is a Smart CNIC?\n"
                "A: A Smart CNIC is a secure identity card embedded with a chip and enhanced biometric security features.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "glossary_final.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# STREAMING RESPONSE (ASYNC)
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You are a glossary assistant. Define NADRA-related terms like CNIC, NICOP, POC, FRC, Smart CNIC, etc. using only the official definitions from the document. "
        "Do not make up definitions or add examples unless clearly present.\n\n"

        "Examples:\n"
        "Q: What is NICOP?\n"
        "A: NICOP is the National Identity Card for Overseas Pakistanis, issued to eligible citizens living abroad.\n\n"
        "Q: What is a Smart CNIC?\n"
        "A: A Smart CNIC is a secure identity card embedded with a chip and enhanced biometric security features."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

