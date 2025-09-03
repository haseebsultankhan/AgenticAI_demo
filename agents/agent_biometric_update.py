import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "biometric_update.md")
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
                "You answer questions about biometric updates at NADRA, using only what's in the official document. "
                "Biometric updates are free if there’s an issue with authentication or if system unavailability caused failure during initial registration."

                "\n\nExamples:\n"
                "Q: Is there a fee for biometric update?\n"
                "A: No, biometric updates are free if there are authentication issues or system unavailability.\n\n"
                "Q: Can I update my fingerprints?\n"
                "A: Yes, biometric updates include fingerprint updates and are free under specific conditions.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "biometric_update.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# STREAMING MODE (async)
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You answer questions about biometric updates at NADRA, using only what's in the official document. "
                "Biometric updates are free if there’s an issue with authentication or if system unavailability caused failure during initial registration."

                "\n\nExamples:\n"
                "Q: Is there a fee for biometric update?\n"
                "A: No, biometric updates are free if there are authentication issues or system unavailability.\n\n"
                "Q: Can I update my fingerprints?\n"
                "A: Yes, biometric updates include fingerprint updates and are free under specific conditions.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk

