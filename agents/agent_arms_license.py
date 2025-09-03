import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "arms_license.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# SYNC FALLBACK
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions strictly based on the official 'Pakistan Arms Rules, 2023' document. "
                "Only provide information explicitly mentioned in the document. Do not speculate or assume anything beyond what's written.\n\n"

                "Examples:\n"
                "Q: What is a business arms licence?\n"
                "A: It is an arms licence issued by the competent authority to a person or organization for dealing in repair, sale, storage, or purchase of arms and ammunition.\n\n"
                
                "Q: Who is considered a legal heir in case of licensee's death?\n"
                "A: A legal heir includes the spouse, parents, children, siblings, or other inheritors of the deceased licensee.\n\n"
                
                "Q: What qualifies as an antique or vintage weapon?\n"
                "A: A weapon that is at least seventy years old is categorized as an antique or vintage weapon.\n\n"
                
                "Q: What does NPO stand for?\n"
                "A: NPO refers to Non-Prohibited Bore weapons."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "arms_license.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# ASYNC STREAMING SUPPORT
# ────────────────────────────────────────────────────────────────────────────────

async def handle_query_stream(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions strictly based on the official 'Pakistan Arms Rules, 2023' document. "
                "Only provide information explicitly mentioned in the document. Do not speculate or assume anything beyond what's written.\n\n"

                "Examples:\n"
                "Q: What is a business arms licence?\n"
                "A: It is an arms licence issued by the competent authority to a person or organization for dealing in repair, sale, storage, or purchase of arms and ammunition.\n\n"
                
                "Q: Who is considered a legal heir in case of licensee's death?\n"
                "A: A legal heir includes the spouse, parents, children, siblings, or other inheritors of the deceased licensee.\n\n"
                
                "Q: What qualifies as an antique or vintage weapon?\n"
                "A: A weapon that is at least seventy years old is categorized as an antique or vintage weapon.\n\n"
                
                "Q: What does NPO stand for?\n"
                "A: NPO refers to Non-Prohibited Bore weapons."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk
