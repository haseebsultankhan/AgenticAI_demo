import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADER
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "Alien_Register.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# SYNC RESPONSE METHOD (existing use, non-streaming fallback)
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions strictly based on the Alien Registration Policy document. "
                "Only reply with information explicitly mentioned in the document. Do not speculate or add assumptions.\n\n"

                "Examples:\n"
                "Q: Who is eligible for alien registration in Pakistan?\n"
                "A: Any foreigner who has lived illegally in Pakistan for at least five years, or has been imprisoned for three years under Foreign Act 14-D, or a foreigner with valid visa/passport intending to stay more than 90 days is eligible.\n\n"
                
                "Q: Is registration mandatory for short stays?\n"
                "A: No. Foreigners intending to stay less than 90 days may optionally register with NADRA.\n\n"
                
                "Q: What documents are required for ARC if someone stayed illegally?\n"
                "A: Documents include expired passport/visa, valid SIM or bank account (both active for at least 5 years), driving license, educational documents, or utility bills in the applicant's name (all at least 5 years old).\n\n"
                
                "Q: Who issues the work permit for foreigners?\n"
                "A: The Interior Division issues work permits to registered foreigners holding an Alien Registration Card (ARC)."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "Alien_Register.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# ASYNC STREAMING RESPONSE METHOD (used by FastAPI StreamingResponse)
# ────────────────────────────────────────────────────────────────────────────────
async def handle_query_stream(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions strictly based on the Alien Registration Policy document. "
                "Only reply with information explicitly mentioned in the document. Do not speculate or add assumptions.\n\n"

                "Examples:\n"
                "Q: Who is eligible for alien registration in Pakistan?\n"
                "A: Any foreigner who has lived illegally in Pakistan for at least five years, or has been imprisoned for three years under Foreign Act 14-D, or a foreigner with valid visa/passport intending to stay more than 90 days is eligible.\n\n"
                
                "Q: Is registration mandatory for short stays?\n"
                "A: No. Foreigners intending to stay less than 90 days may optionally register with NADRA.\n\n"
                
                "Q: What documents are required for ARC if someone stayed illegally?\n"
                "A: Documents include expired passport/visa, valid SIM or bank account (both active for at least 5 years), driving license, educational documents, or utility bills in the applicant's name (all at least 5 years old).\n\n"
                
                "Q: Who issues the work permit for foreigners?\n"
                "A: The Interior Division issues work permits to registered foreigners holding an Alien Registration Card (ARC)."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk

