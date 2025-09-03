import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "change_in_card_final.md")
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
                "You are a NADRA assistant answering only questions about changes allowed in CNIC details. "
                "You must strictly use the information provided in the official change rules. Do not assume anything outside the context."

                "\n\nExamples:\n"
                "Q: Can I change my father's name on my CNIC?\n"
                "A: Father’s name change is allowed if proper documentary proof is provided.\n\n"
                "Q: Can I change my gender?\n"
                "A: Yes, NADRA allows gender updates with valid documentation and review.\n\n"
                "Q: Can I modify my address?\n"
                "A: Yes, address changes are permitted with recent utility bills or rent agreements as proof.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "change_in_card_final.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# ASYNC STREAMING MODE
# ────────────────────────────────────────────────────────────────────────────────

async def handle_query_stream(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering only questions about changes allowed in CNIC details. "
                "You must strictly use the information provided in the official change rules. Do not assume anything outside the context."

                "\n\nExamples:\n"
                "Q: Can I change my father's name on my CNIC?\n"
                "A: Father’s name change is allowed if proper documentary proof is provided.\n\n"
                "Q: Can I change my gender?\n"
                "A: Yes, NADRA allows gender updates with valid documentation and review.\n\n"
                "Q: Can I modify my address?\n"
                "A: Yes, address changes are permitted with recent utility bills or rent agreements as proof.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk

