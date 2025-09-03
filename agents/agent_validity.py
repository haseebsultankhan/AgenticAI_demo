# agents/agent_validity.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

def load_context():
    file_path = os.path.join("data", "validity_final.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ─────────────────────────────────────────────────────────────────────────────
# Sync API Response
# ─────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You provide information about the validity period of CNIC, NICOP, and POC. Use only the official validity durations as per age and card type. "
                "Never assume expiry periods or create unofficial guidance.\n\n"

                "Examples:\n"
                "Q: How long is a CNIC valid?\n"
                "A: For individuals below 53, a CNIC remains valid for 10 years; for those over 53, it's valid for life. Renew before expiration to prevent future issues.\n\n"
                "Q: What’s the validity of NICOP for someone over 50?\n"
                "A: For applicants above 50 years, NICOP is valid for life.\n\n"
                "Q: When does a POC expire?\n"
                "A: POC validity is defined based on issuance guidelines; refer to NADRA rules for individual cases.\n\n"
                "Q: How long is a CNIC valid for a 53 year old or above?\n"
                "A: CNIC is valid for life for applicants above 53 years upon renewal of the CNIC.\n\n"
                "Q: I have a CNIC, which is not yet expired, but I am 53 years old. Do I need to renew it?\n"
                "A: No, you do not need to renew your CNIC if it is not expired. But you need to renew your CNIC at least before a month of expiry. Upon renewal, you will receive a CNIC with lifetime validity.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "validity_final.md",
        "answer": get_llm_response(messages)
    }

# ─────────────────────────────────────────────────────────────────────────────
# Async Streaming Response
# ─────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You provide information about the validity period of CNIC, NICOP, and POC. Use only the official validity durations as per age and card type. "
        "Never assume expiry periods or create unofficial guidance."

        "\n\nExamples:\n"
        "Q: How long is a CNIC valid?\n"
        "A: For individuals below 53, a CNIC remains valid for 10 years; for those over 53, it's valid for life. Renew before expiration to prevent future issues.\n\n"
        "Q: What’s the validity of NICOP for someone over 50?\n"
        "A: For applicants above 50 years, NICOP is valid for life.\n\n"
        "Q: When does a POC expire?\n"
        "A: POC validity is defined based on issuance guidelines; refer to NADRA rules for individual cases.\n"
        "Q: How long is a CNIC valid for a 53 year old or above?\n"
        "A: CNIC is valid for life for applicants above 53 years upon renawal of the CNIC\n\n"
        "Q: I have a CNIC , which is not yet expired, but I am 53 years old. Do I need to renew it?\n"
        "A: No, you do not need to renew your CNIC if it is not expired. But you need to renew your CNIC atleast before a month of expiry, upon renawal you will recieve a CNIC with lifetime validity\n\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

