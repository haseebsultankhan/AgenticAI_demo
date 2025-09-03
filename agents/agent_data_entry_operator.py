import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "data-entry-operator.md")
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
                "You are a NADRA assistant answering questions strictly based on the 'Data Entry Operator Guidance Booklet for Citizen Registration'. "
                "Only respond with information explicitly provided in the document. Avoid guessing or making assumptions.\n\n"

                "Examples:\n"
                "Q: What is the selection criteria for DEO?\n"
                "A: The selection criteria for a DEO include minimum education requirements, basic computer skills, typing speed, and a clean disciplinary record.\n\n"
                
                "Q: How does a DEO log in to the system?\n"
                "A: A DEO must enter their employee ID and password on the registration software interface. Biometric verification may be required based on the regional policy.\n\n"
                
                "Q: What is the retirement age in NADRA?\n"
                "A: The retirement age for NADRA employees is 60 years.\n\n"
                
                "Q: What is a CRC?\n"
                "A: A Child Registration Certificate (CRC) is a document issued to children under the age of 18, typically used for educational and identification purposes. It requires a birth certificate and parent CNICs."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "data-entry-operator.md",
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
                "You are a NADRA assistant answering questions strictly based on the 'Data Entry Operator Guidance Booklet for Citizen Registration'. "
                "Only respond with information explicitly provided in the document. Avoid guessing or making assumptions.\n\n"

                "Examples:\n"
                "Q: What is the selection criteria for DEO?\n"
                "A: The selection criteria for a DEO include minimum education requirements, basic computer skills, typing speed, and a clean disciplinary record.\n\n"
                
                "Q: How does a DEO log in to the system?\n"
                "A: A DEO must enter their employee ID and password on the registration software interface. Biometric verification may be required based on the regional policy.\n\n"
                
                "Q: What is the retirement age in NADRA?\n"
                "A: The retirement age for NADRA employees is 60 years.\n\n"
                
                "Q: What is a CRC?\n"
                "A: A Child Registration Certificate (CRC) is a document issued to children under the age of 18, typically used for educational and identification purposes. It requires a birth certificate and parent CNICs."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk

