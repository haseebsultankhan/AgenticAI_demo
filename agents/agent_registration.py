# agents/agent_registeration_process.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

def load_context():
    file_path = os.path.join("data", "registeration_process_final.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ─────────────────────────────────────────────────────────────────────────────
# Sync Response (used in controller or normal API call)
# ─────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You assist with the full CNIC registration process at NADRA centers. "
                "Only describe steps outlined in the official registration document. Do not add services or speculate on steps."

                "\n\nExamples:\n"
                "Q: How do I register for CNIC?\n"
                "A: Visit a NADRA Registration Center. You'll get a token, followed by biometric capture, data entry, interview, and document upload.\n\n"
                "Q: Can I get CNIC without biometrics?\n"
                "A: No, biometric verification is mandatory in the CNIC registration process.\n\n"
                "Q: What happens after I apply?\n"
                "A: Your application is uploaded to NADRA’s central system for further verification and processing.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "registeration_process_final.md",
        "answer": get_llm_response(messages)
    }

# ─────────────────────────────────────────────────────────────────────────────
# Async Streaming Response (used for real-time chat)
# ─────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You assist with the full CNIC registration process at NADRA centers. "
        "Only describe steps outlined in the official registration document. Do not add services or speculate on steps."

        "\n\nExamples:\n"
        "Q: How do I register for CNIC?\n"
        "A: Visit a NADRA Registration Center. You'll get a token, followed by biometric capture, data entry, interview, and document upload.\n\n"
        "Q: Can I get CNIC without biometrics?\n"
        "A: No, biometric verification is mandatory in the CNIC registration process.\n\n"
        "Q: What happens after I apply?\n"
        "A: Your application is uploaded to NADRA’s central system for further verification and processing.\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk
