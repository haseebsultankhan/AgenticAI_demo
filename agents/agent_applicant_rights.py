import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "applicant_rights_final.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# SYNC MODE (fallback)
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions based strictly on the applicant rights document. "
                "Only reply with rights explicitly listed in the document. Don't generalize or speculate."

                "\n\nExamples:\n"
                "Q: What rights do I have at NADRA?\n"
                "A: You have the right to fair treatment, data privacy, and to submit complaints and receive timely resolutions.\n\n"
                "Q: Can I know how my data is used?\n"
                "A: Yes, applicants have the right to access and correct their personal records, and have their data protected from unauthorized access.\n\n"
                "Q: Can I complain if I feel mistreated?\n"
                "A: Yes, NADRA guarantees the right to grievance redressal and fair service accountability.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "applicant_rights_final.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# ASYNC STREAMING MODE (preferred)
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions based strictly on the applicant rights document. "
                "Only reply with rights explicitly listed in the document. Don't generalize or speculate."

                "\n\nExamples:\n"
                "Q: What rights do I have at NADRA?\n"
                "A: You have the right to fair treatment, data privacy, and to submit complaints and receive timely resolutions.\n\n"
                "Q: Can I know how my data is used?\n"
                "A: Yes, applicants have the right to access and correct their personal records, and have their data protected from unauthorized access.\n\n"
                "Q: Can I complain if I feel mistreated?\n"
                "A: Yes, NADRA guarantees the right to grievance redressal and fair service accountability.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk

