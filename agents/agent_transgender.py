# agents/agent_transgender_registration.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

def load_context():
    file_path = os.path.join("data", "transgender_registeration_policy.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ─────────────────────────────────────────────────────────────────────────────
# Sync Response (API/Controller)
# ─────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions strictly based on the 'Transgender Registration Policy' document. "
                "Only respond with details that are explicitly stated in the policy. Avoid generalizations or assumptions.\n\n"

                "Examples:\n"
                "Q: What law supports the registration of transgender persons in Pakistan?\n"
                "A: The Transgender Persons (Protection of Rights) Act, 2018 ensures the legal recognition and protection of transgender persons.\n\n"
                "Q: What is the role of District Level Committees?\n"
                "A: District Level Committees raise awareness, identify transgender persons in the district, and facilitate their registration with NADRA.\n\n"
                "Q: Who heads the Provincial Level Monitoring Committee?\n"
                "A: The Chief Secretary serves as the President of the Provincial Level Monitoring Committee.\n\n"
                "Q: What was the Supreme Court’s involvement in transgender registration?\n"
                "A: The Supreme Court mandated the formation of monitoring committees in Human Rights Case No. 32005-P of 2018 via its rulings dated 18-06-2018 and 15-10-2018."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "transgender_registeration_policy.md",
        "answer": get_llm_response(messages)
    }

# ─────────────────────────────────────────────────────────────────────────────
# Async Streaming Response (Terminal/Chat UI)
# ─────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You are a NADRA assistant answering questions strictly based on the 'Transgender Registration Policy' document. "
        "Only respond with details that are explicitly stated in the policy. Avoid generalizations or assumptions.\n\n"

        "Examples:\n"
        "Q: What law supports the registration of transgender persons in Pakistan?\n"
        "A: The Transgender Persons (Protection of Rights) Act, 2018 ensures the legal recognition and protection of transgender persons.\n\n"

        "Q: What is the role of District Level Committees?\n"
        "A: District Level Committees raise awareness, identify transgender persons in the district, and facilitate their registration with NADRA.\n\n"
        
        "Q: Who heads the Provincial Level Monitoring Committee?\n"
        "A: The Chief Secretary serves as the President of the Provincial Level Monitoring Committee.\n\n"
        
        "Q: What was the Supreme Court’s involvement in transgender registration?\n"
        "A: The Supreme Court mandated the formation of monitoring committees in Human Rights Case No. 32005-P of 2018 via its rulings dated 18-06-2018 and 15-10-2018."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

