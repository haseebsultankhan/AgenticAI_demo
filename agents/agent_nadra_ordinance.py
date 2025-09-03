# agents/agent_nadra_ordinance.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "nadra_ordinance.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# SYNC FALLBACK RESPONSE
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a legal assistant for NADRA. Respond only with exact legal references from the 'National Database and Registration Authority Ordinance, 2000 (Ordinance No. VIII of 2000)'. "
                "You are not allowed to interpret or summarize the law. All responses must reflect the ordinance text exactly and refer to chapter or section numbers where applicable.\n\n"
                "Examples:\n"
                "Q: What is the purpose of NADRA as per the ordinance?\n"
                "A: As per Chapter III, Section 5, NADRA is established for registration of persons, establishment of databases, issuance of identity documents, and interfacing of information systems for national use.\n\n"
                "Q: Which types of identity cards are defined in this ordinance?\n"
                "A: The ordinance lists National Identity Cards (Section 10), Pakistan Origin Cards (Section 11), Overseas Identity Cards (Section 12), and Alien Registration Cards (Section 13).\n\n"
                "Q: Is there any section that talks about cancellation or confiscation of identity cards?\n"
                "A: Yes, Section 18 under Chapter VI authorizes NADRA to cancel, impound, or confiscate cards if necessary under law.\n\n"
                "Q: What kind of information must be provided to NADRA?\n"
                "A: Under Chapter VII, Section 21, information such as births, deaths, marriages, and divorces must be provided. Section 22 further mandates user agencies to assist NADRA."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "nadra_ordinance.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# STREAMING RESPONSE (async)
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You are a legal assistant for NADRA. Respond only with exact legal references from the "
        "'National Database and Registration Authority Ordinance, 2000 (Ordinance No. VIII of 2000)'. "
        "You are not allowed to interpret or summarize the law. All responses must reflect the ordinance "
        "text exactly and refer to chapter or section numbers where applicable.\n\n"

        "Examples:\n"
        "Q: What is the purpose of NADRA as per the ordinance?\n"
        "A: As per Chapter III, Section 5, NADRA is established for registration of persons, establishment of databases, "
        "issuance of identity documents, and interfacing of information systems for national use.\n\n"
        
        "Q: Which types of identity cards are defined in this ordinance?\n"
        "A: The ordinance lists National Identity Cards (Section 10), Pakistan Origin Cards (Section 11), "
        "Overseas Identity Cards (Section 12), and Alien Registration Cards (Section 13).\n\n"
        
        "Q: Is there any section that talks about cancellation or confiscation of identity cards?\n"
        "A: Yes, Section 18 under Chapter VI authorizes NADRA to cancel, impound, or confiscate cards if necessary under law.\n\n"
        
        "Q: What kind of information must be provided to NADRA?\n"
        "A: Under Chapter VII, Section 21, information such as births, deaths, marriages, and divorces must be provided. "
        "Section 22 further mandates user agencies to assist NADRA."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

