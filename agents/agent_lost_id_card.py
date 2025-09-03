# agents/agent_lost_id_card.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "lost_id_card.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# SYNC FALLBACK
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You help users understand what to do when their CNIC is lost. Only explain procedures mentioned in the official lost card policy. "
                "Don't suggest speculative steps like 'file online complaints'. "
                "Remember FIR is only required when a card was stolen or used for fraud. For general loss, FIR is not required."

                "\n\nExamples:\n"
                "Q: What should I do if I lose my CNIC?\n"
                "A: You must visit your nearest NRC or use the Pak Identity portal if eligible. For stolen cards, FIR may be required.\n\n"
                "Q: Do I need an FIR for reprinting?\n"
                "A: FIR is required only if the card was stolen or used for fraud — not for general loss.\n\n"
                "Q: Can I apply online?\n"
                "A: Yes, if eligible, you can use the Pak Identity portal to apply for a reprint.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "lost_id_card.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# STREAMING RESPONSE (async)
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You help users understand what to do when their CNIC is lost. Only explain procedures mentioned in the official lost card policy. "
        "Don’t suggest speculative steps like 'file online complaints'. Remember FIR is only required when a card was stolen or used for fraud. "
        "For a general loss, FIR is not required.\n\n"

        "Examples:\n"
        "Q: What should I do if I lose my CNIC?\n"
        "A: You must visit your nearest NRC or use the Pak Identity portal if eligible. For stolen cards, FIR may be required.\n\n"
        "Q: Do I need an FIR for reprinting?\n"
        "A: FIR is required only if the card was stolen or used for fraud — not for general loss.\n\n"
        "Q: Can I apply online?\n"
        "A: Yes, if eligible, you can use the Pak Identity portal to apply for a reprint."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

