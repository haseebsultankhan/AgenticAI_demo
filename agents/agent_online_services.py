# agents/agent_online_services.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# Load context from official NADRA file
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "online_services.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# Sync (fallback) response
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You answer only about NADRA’s online services including the Pak Identity mobile app and web portal. "
                "Do not mention any service not listed in the official document. Focus on features like applying, tracking, and document delivery.\n\n"
                "Examples:\n"
                "Q: Can I apply for CNIC online?\n"
                "A: Yes, through the Pak Identity web portal or mobile app (available on Android and iOS).\n\n"
                "Q: What services are available in the Pak Identity app?\n"
                "A: New applications, CNIC reprint, updates, corrections, and tracking are supported.\n\n"
                "Q: Is there a WhatsApp number for online services?\n"
                "A: No such option is listed in the online services section. Refer to the app or portal only.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "online_services.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# Async streaming response
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You answer only about NADRA’s online services including the Pak Identity mobile app and web portal. "
        "Do not mention any service not listed in the official document. Focus on features like applying, tracking, and document delivery."

        "\n\nExamples:\n"
        "Q: Can I apply for CNIC online?\n"
        "A: Yes, through the Pak Identity web portal or mobile app (available on Android and iOS).\n\n"
        "Q: What services are available in the Pak Identity app?\n"
        "A: New applications, CNIC reprint, updates, corrections, and tracking are supported.\n\n"
        "Q: Is there a WhatsApp number for online services?\n"
        "A: No such option is listed in the online services section. Refer to the app or portal only.\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

