# agents/agent_renewal.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

def load_context():
    file_path = os.path.join("data", "renewal_questions.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ─────────────────────────────────────────────────────────────────────────────
# Sync Response (used for controller or API)
# ─────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You provide information when a person needs to know when to renew their CNIC, NICOP, POC, Succession Certificate, and Birth Certificate (CRC = Child Registration Certificate). "
                "Use only the official renewal guidelines as per age and card type. Never assume expiry periods or create unofficial guidance."

                "\n\nExamples:\n"

                "Q: What is the validity of a CNIC?\n"
                "A: CNIC is valid for 10 years for adults aged 18 to 52, and for a lifetime for adults aged 53 and above.\n\n"

                "Q: When should I renew my CNIC?\n"
                "A: CNIC can be renewed up to 1 month before expiry, or earlier in case of changes to name, photo, marital status, address, or if lost/damaged.\n\n"

                "Q: What is the validity of a NICOP?\n"
                "A: NICOP is valid for 10 years for adults and 5 years for minors under 18.\n\n"

                "Q: When should I renew my POC?\n"
                "A: POC should be renewed up to 6 months before expiry or earlier in case of changes in passport or personal details.\n\n"

                "Q: Does FRC have an expiry date?\n"
                "A: No, FRC has no formal expiry and remains valid unless family information changes.\n\n"

                "Q: When would I need to reissue a Succession Certificate?\n"
                "A: You may need a reissuance if new assets are discovered, legal disputes arise, or corrections are needed.\n\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "renewal_questions.md",
        "answer": get_llm_response(messages)
    }

# ─────────────────────────────────────────────────────────────────────────────
# Streaming Response (used for terminal/async chat interface)
# ─────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You provide information when a person needs to know when to review their CNIC, NICOP, POC, Succession Certificate, and Birth Certificate (CRC = Child Registration Certificate). "
        "Use only the official renewal guidelines as per age and card type. Never assume expiry periods or create unofficial guidance."

        "\n\nExamples:\n"

        # CNIC
        "Q: What is the validity of a CNIC?\n"
        "A: CNIC is valid for 10 years for adults aged 18 to 52, and for a lifetime for adults aged 53 and above.\n\n"

        "Q: When should I renew my CNIC?\n"
        "A: CNIC can be renewed up to 1 month before expiry, or earlier in case of changes to name, photo, marital status, address, or if lost/damaged.\n\n"

        "Q: Is there a lifetime CNIC?\n"
        "A: Yes, for applicants aged 53 and above, CNIC is valid for a lifetime.\n\n"

        "Q: Do I need to renew CNIC if my address changes?\n"
        "A: Yes, you must renew your CNIC to reflect your updated address.\n\n"

        # CRC
        "Q: What is the validity of a CRC?\n"
        "A: CRC is valid until the child turns 18.\n\n"

        "Q: What happens to CRC after age 18?\n"
        "A: CRC must be replaced by a CNIC when the child turns 18. It is important to apply for the CNIC no later than 30 days after turning 18.\n\n"

        # FRC
        "Q: Does FRC have an expiry date?\n"
        "A: No, FRC has no formal expiry and remains valid unless family information changes.\n\n"

        "Q: When should I update or reapply for FRC?\n"
        "A: You should reapply if there’s a major family change such as a birth, marriage, divorce, or death.\n\n"

        # NICOP
        "Q: What is the validity of a NICOP?\n"
        "A: NICOP is valid for 10 years for adults and 5 years for minors under 18.\n\n"

        "Q: When can I renew NICOP?\n"
        "A: NICOP can be renewed up to 6 months before expiry, or earlier in case of changes in passport, marital status, name, or photo.\n\n"

        "Q: Can I renew NICOP after a passport change?\n"
        "A: Yes, a change in passport details requires updating your NICOP.\n\n"

        # POC
        "Q: How long is a POC valid?\n"
        "A: POC is valid for 5 years regardless of the applicant’s age.\n\n"

        "Q: When should I renew my POC?\n"
        "A: POC should be renewed up to 6 months before expiry or earlier in case of changes in passport or personal details.\n\n"

        # Succession Certificate
        "Q: Does the NADRA Succession Certificate expire?\n"
        "A: No, the Succession Certificate has no formal expiry and remains permanently valid.\n\n"

        "Q: When would I need to reissue a Succession Certificate?\n"
        "A: You may need a reissuance if new assets are discovered, legal disputes arise, or corrections are needed.\n\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

