# agents/agent_succession_certificate.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

def load_context():
    file_path = os.path.join("data", "succession_certificate.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ─────────────────────────────────────────────────────────────────────────────
# Sync Response (used in controller/API)
# ─────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions strictly based on the 'Succession Registration SOP' (Version SFU-1.0.1, February 2024). "
                "Only respond with information directly mentioned in the document. Do not guess or elaborate beyond the official policy.\n\n"

                "Examples:\n"
                "Q: Who is considered a legal heir according to this policy?\n"
                "A: A legal heir is a person who has entitlement to a share in the property of the deceased.\n\n"
                
                "Q: What is an SFU?\n"
                "A: SFU stands for Succession Facilitation Unit, which is established for receiving, assessing, and processing applications for Letters of Administration, Succession Certificates, and Decline Certificates.\n\n"
                
                "Q: What is a factual controversy?\n"
                "A: It refers to objections by legal heirs or claimants, or any dispute requiring court adjudication, including cases where at least one legal heir is a minor.\n\n"
                
                "Q: Which regions are covered under this policy?\n"
                "A: The policy applies across the whole of ICT, Punjab, Sindh, Khyber Pakhtunkhwa, Balochistan, AJK, and Gilgit-Baltistan."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "succession_certificate.md",
        "answer": get_llm_response(messages)
    }

# ─────────────────────────────────────────────────────────────────────────────
# Async Streaming Response (used in terminal/chat UI)
# ─────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You are a NADRA assistant answering questions strictly based on the 'Succession Registration SOP' (Version SFU-1.0.1, February 2024). "
        "Only respond with information directly mentioned in the document. Do not guess or elaborate beyond the official policy.\n\n"

        "Examples:\n"
        "Q: Who is considered a legal heir according to this policy?\n"
        "A: A legal heir is a person who has entitlement to a share in the property of the deceased.\n\n"
        
        "Q: What is an SFU?\n"
        "A: SFU stands for Succession Facilitation Unit, which is established for receiving, assessing, and processing applications for Letters of Administration, Succession Certificates, and Decline Certificates.\n\n"
        
        "Q: What is a factual controversy?\n"
        "A: It refers to objections by legal heirs or claimants, or any dispute requiring court adjudication, including cases where at least one legal heir is a minor.\n\n"
        
        "Q: Which regions are covered under this policy?\n"
        "A: The policy applies across the whole of ICT, Punjab, Sindh, Khyber Pakhtunkhwa, Balochistan, AJK, and Gilgit-Baltistan."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

