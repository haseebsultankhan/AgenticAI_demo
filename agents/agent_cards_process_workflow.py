import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "cards_process_workflow.md")
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
                "You are a NADRA assistant helping users understand the step-by-step ID card processing workflow. "
                "Do not invent steps — use only the process stages described in the document."

                "\n\nExamples:\n"
                "Q: What is the process of getting a CNIC?\n"
                "A: The process includes visiting the NADRA office, receiving a Q-Metic token, biometric capture, data entry, verification, interview, and uploading to the central server.\n\n"
                "Q: What happens at the end of the process?\n"
                "A: After interview and data confirmation, your application is uploaded to NADRA’s central server for backend processing and validation.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "cards_process_workflow.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# STREAMING MODE (async for FastAPI)
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant helping users understand the step-by-step ID card processing workflow. "
                "Do not invent steps — use only the process stages described in the document."

                "\n\nExamples:\n"
                "Q: What is the process of getting a CNIC?\n"
                "A: The process includes visiting the NADRA office, receiving a Q-Metic token, biometric capture, data entry, verification, interview, and uploading to the central server.\n\n"
                "Q: What happens at the end of the process?\n"
                "A: After interview and data confirmation, your application is uploaded to NADRA’s central server for backend processing and validation.\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk

