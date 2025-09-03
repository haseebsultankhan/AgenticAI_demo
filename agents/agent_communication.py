# agents/agent_communication.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "communication_and_complaints.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# SYNC RESPONSE (fallback)
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You help users reach NADRA through official communication channels. "
                "Only refer to listed contact methods such as NCCMS, call centers, and WhatsApp channel. "
                "Do not create options outside the provided data."

                "\n\nExamples:\n"
                "Q: How do I complain to NADRA?\n"
                "A: Use the NCCMS portal at https://complaints.nadra.gov.pk or dial 1777/051-111-786-100.\n\n"
                "Q: What is NADRA's WhatsApp channel?\n"
                "A: Follow US <a href='https://www.whatsapp.com/channel/0029VaH7JG2I1rckS9XnTg23'>Whatsapp</a>\n\n"
                "Q: Can I reach NADRA through social media?\n"
                "A: Yes, via Facebook (@NadraPakistanOfficial) or Twitter (@NadraPak).\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "communication_and_complaints.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# STREAMING RESPONSE (preferred in FastAPI)
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You help users reach NADRA through official communication channels. Only refer to listed contact methods such as NCCMS, call centers, and WhatsApp channel. Do not create options outside the provided data."

                "\n\nExamples:\n"
                "Q: How do I complain to NADRA?\n"
                "A: Use the NCCMS portal at https://complaints.nadra.gov.pk or dial 1777/051-111-786-100.\n\n"
                "Q: What is NADRA's WhatsApp channel?\n"
                "A: Follow Us bit.ly/4mtMsKF \n\n"
                "Q: Can I reach NADRA through social media?\n"
                "A: Yes, via Facebook (@NadraPakistanOfficial) or Twitter (@NadraPak).\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk

