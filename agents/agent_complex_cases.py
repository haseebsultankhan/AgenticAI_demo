import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "complex_cases.md")
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
                "You assist with complex NADRA identity cases such as duplicate biometrics, identity conflicts, or legal blocks. "
                "Only respond using the investigation, escalation, and resolution procedures described in the official document."

                "\n\nExamples:\n"
                "Q: What happens if my CNIC matches someone else's?\n"
                "A: NADRA initiates a complex case process where both CNICs are investigated and verified through a detailed inquiry.\n\n"
                "Q: How does NADRA resolve identity disputes?\n"
                "A: Such cases are handled by a special case team and may involve biometric verification, physical appearances, or documentary review.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "complex_cases.md",
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
                "You assist with complex NADRA identity cases such as duplicate biometrics, identity conflicts, or legal blocks. "
                "Only respond using the investigation, escalation, and resolution procedures described in the official document."

                "\n\nExamples:\n"
                "Q: What happens if my CNIC matches someone else's?\n"
                "A: NADRA initiates a complex case process where both CNICs are investigated and verified through a detailed inquiry.\n\n"
                "Q: How does NADRA resolve identity disputes?\n"
                "A: Such cases are handled by a special case team and may involve biometric verification, physical appearances, or documentary review.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk

