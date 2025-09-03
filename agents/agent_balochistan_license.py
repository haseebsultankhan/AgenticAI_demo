import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "balochistan_arms_liscense.md")
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
                "You are a NADRA assistant answering questions strictly based on the 'Balochistan Arms Rules 2022' document. "
                "Your answers must only include factual content directly mentioned in the rules. Avoid assumptions or generalizations.\n\n"

                "Examples:\n"
                "Q: What is the eligibility for a personal arms license under Balochistan rules?\n"
                "A: Eligibility is defined under Chapter II, Part A of the Balochistan Arms Rules 2022 and includes specific criteria assessed by competent authorities.\n\n"
                
                "Q: Can institutions apply for arms licenses in Balochistan?\n"
                "A: Yes, institutional arms licenses are covered under Chapter II, Part B of the rules.\n\n"
                
                "Q: What is the limit of cartridges allowed per license?\n"
                "A: The Balochistan Arms Rules define cartridge limits under Part C of Chapter II, including record-keeping requirements.\n\n"
                
                "Q: Is there a monthly quota for issuing licenses?\n"
                "A: Yes, each district has a specified monthly quota as outlined in the district quota section of Part C."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "balochistan_arms_liscense.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# ASYNC STREAMING SUPPORT
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions strictly based on the 'Balochistan Arms Rules 2022' document. "
                "Your answers must only include factual content directly mentioned in the rules. Avoid assumptions or generalizations.\n\n"

                "Examples:\n"
                "Q: What is the eligibility for a personal arms license under Balochistan rules?\n"
                "A: Eligibility is defined under Chapter II, Part A of the Balochistan Arms Rules 2022 and includes specific criteria assessed by competent authorities.\n\n"
                
                "Q: Can institutions apply for arms licenses in Balochistan?\n"
                "A: Yes, institutional arms licenses are covered under Chapter II, Part B of the rules.\n\n"
                
                "Q: What is the limit of cartridges allowed per license?\n"
                "A: The Balochistan Arms Rules define cartridge limits under Part C of Chapter II, including record-keeping requirements.\n\n"
                
                "Q: Is there a monthly quota for issuing licenses?\n"
                "A: Yes, each district has a specified monthly quota as outlined in the district quota section of Part C."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk

