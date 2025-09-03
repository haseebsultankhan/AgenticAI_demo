# agents/agent_products.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# Load context from products.md
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "products.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# Sync response for traditional usage
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You provide descriptions of NADRA’s identity-related products such as CNIC, NICOP, CRC, FRC, POC and succession certificate.\n"
                "Only use definitions or product features listed in the official document. Do not speculate."

                "\n\nExamples:\n"
                "Q: What is a CRC?\n"
                "A: CRC stands for Child Registration Certificate, issued for citizens under 18.\n\n"
                "Q: What documents are issued for dual nationals?\n"
                "A: NICOP is issued to dual nationals; POC is for non-citizens of Pakistani origin.\n\n"
                "Q: What’s the difference between NICOP and CNIC?\n"
                "A: NICOP is for overseas Pakistanis, while CNIC is for residents.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "products.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# Async streaming generator for real-time LLM output
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You provide descriptions of NADRA’s identity-related products such as CNIC, NICOP, CRC, FRC, POC and succession certificate.\n"
        "Only use definitions or product features listed in the official document. Do not speculate."

        "\n\nExamples:\n"
        "Q: What is a CRC?\n"
        "A: CRC stands for Child Registration Certificate, issued for citizens under 18.\n\n"
        "Q: What documents are issued for dual nationals?\n"
        "A: NICOP is issued to dual nationals; POC is for non-citizens of Pakistani origin.\n\n"
        "Q: What’s the difference between NICOP and CNIC?\n"
        "A: NICOP is for overseas Pakistanis, while CNIC is for residents.\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

