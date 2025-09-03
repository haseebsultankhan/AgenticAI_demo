# agents/agent_sms_short_codes.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

def load_context():
    file_path = os.path.join("data", "sms_short_codes_final.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ─────────────────────────────────────────────────────────────────────────────
# Sync Response (used in controller/API)
# ─────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You explain NADRA's official SMS short codes. Only respond about codes explicitly mentioned in the document like 8009, 8400, 8300, 1166, etc. "
                "If a code is not in the list, reply that no information is provided.\n\n"

                "Examples:\n"
                "Q: What does 8400 do?\n"
                "A: 8400 is used to check CNIC application status via SMS.\n\n"
                "Q: What is 8009 for?\n"
                "A: 8009 is for election-related CNIC registration awareness.\n\n"
                "Q: What is 7000 used for?\n"
                "A: There is no information about short code 7000 in the official NADRA SMS services list.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "sms_short_codes_final.md",
        "answer": get_llm_response(messages)
    }

# ─────────────────────────────────────────────────────────────────────────────
# Async Streaming Response (used in terminal/chat UI)
# ─────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You explain NADRA's official SMS short codes. Only respond about codes explicitly mentioned in the document like 8009, 8400, 8300, 1166, etc. "
        "If a code is not in the list, reply that no information is provided."

        "\n\nExamples:\n"
        "Q: What does 8400 do?\n"
        "A: 8400 is used to check CNIC application status via SMS.\n\n"
        "Q: What is 8009 for?\n"
        "A: 8009 is for election-related CNIC registration awareness.\n\n"
        "Q: What is 7000 used for?\n"
        "A: There is no information about short code 7000 in the official NADRA SMS services list.\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

