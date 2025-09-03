# agents/agent_processing_time.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# Load processing time context from markdown
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "processing_time_final.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# Sync response for backward compatibility
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You respond with NADRA’s official processing times only. Don’t guess durations or offer unverified timelines. "
                "Mention normal, urgent, executive timelines as per CNIC, NICOP, POC categories listed in the document."

                "\n\nExamples:\n"
                "Q: How long does urgent CNIC take?\n"
                "A: Urgent CNIC is processed in 7 working days as per official standard.\n\n"
                "Q: How long is executive NICOP processing?\n"
                "A: Executive NICOP takes 2 working days in Pakistan. Overseas times may vary.\n\n"
                "Q: How many days for normal CNIC?\n"
                "A: Around 30 days as listed in NADRA processing chart.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "processing_time_final.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# Async streaming generator for real-time LLM output
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You respond with NADRA’s official processing times only. Don’t guess durations or offer unverified timelines. "
        "Mention normal, urgent, executive timelines as per CNIC, NICOP, POC categories listed in the document."

        "\n\nExamples:\n"
        "Q: How long does urgent CNIC take?\n"
        "A: Urgent CNIC is processed in 7 working days as per official standard.\n\n"
        "Q: How long is executive NICOP processing?\n"
        "A: Executive NICOP takes 2 working days in Pakistan. Overseas times may vary.\n\n"
        "Q: How many days for normal CNIC?\n"
        "A: Around 30 days as listed in NADRA processing chart.\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

