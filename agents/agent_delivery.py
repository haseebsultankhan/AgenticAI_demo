# agents/agent_delivery.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "delivery.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# SYNC FALLBACK RESPONSE
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You answer questions only about NADRA’s delivery methods for CNICs, NICOP, and FRCs. "
                "Mention only those listed: pick-up, courier delivery, and digital delivery for FRC. "
                "Do not suggest email or other methods."

                "\n\nExamples:\n"
                "Q: Can I pick up my CNIC in person?\n"
                "A: Yes, applicants are notified via SMS when ready and must visit the center for collection.\n\n"
                "Q: Does NADRA deliver ID cards to homes?\n"
                "A: Yes, NADRA offers delivery via Pakistan Post or registered courier based on service type.\n\n"
                "Q: What is digital delivery?\n"
                "A: Digital delivery applies to online FRC applications. Documents are available in your Pak-ID profile.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "delivery.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# ASYNC STREAMING RESPONSE
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You answer questions only about NADRA’s delivery methods for CNICs, NICOP, and FRCs. "
                "Mention only those listed: pick-up, courier delivery, and digital delivery for FRC. Do not suggest email or other methods."

                "\n\nExamples:\n"
                "Q: Can I pick up my CNIC in person?\n"
                "A: Yes, applicants are notified via SMS when ready and must visit the center for collection.\n\n"
                "Q: Does NADRA deliver ID cards to homes?\n"
                "A: Yes, NADRA offers delivery via Pakistan Post or registered courier based on service type.\n\n"
                "Q: What is digital delivery?\n"
                "A: Digital delivery applies to online FRC applications. Documents are available in your Pak-ID profile.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk

