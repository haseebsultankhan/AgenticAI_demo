# agents/agent_orphanage_policy.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# Load the official NADRA orphanage policy content
# ────────────────────────────────────────────────────────────────────────────────

def load_context():
    file_path = os.path.join("data", "orphange_policy.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# Sync (fallback) response for basic usage
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions strictly based on the 'Orphanage Registration Policy' document dated 24/02/2016. "
                "All answers must be based only on the policy content — do not speculate or generalize beyond the official procedures.\n\n"

                "Examples:\n"
                "Q: What documents are required to register an orphanage with NADRA?\n"
                "A: The orphanage must submit an application, its registration certificate with the Federal or Provincial Government, and a filled Orphanage Registration Form (Annex-A) with guardian details.\n\n"
                
                "Q: Who approves the registration of an orphanage in the NADRA database?\n"
                "A: The registration is approved by the Chief Operating Officer or DG (Ops) at NADRA HQ.\n\n"
                
                "Q: What is the purpose of orphan registration with NADRA?\n"
                "A: It ensures legal identity and helps safeguard orphan children’s fundamental rights like education, healthcare, and social protection.\n\n"
                
                "Q: Was this policy legally endorsed?\n"
                "A: Yes, the policy was presented before the Supreme Court of Pakistan (Human Rights Case No. 22607-S/2011) and the Lahore High Court (W.P. No. 20197/2014) and was endorsed accordingly."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "orphange_policy.md",
        "answer": get_llm_response(messages)
    }

# ────────────────────────────────────────────────────────────────────────────────
# Async streaming method for full concurrency use with Ollama
# ────────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You are a NADRA assistant answering questions strictly based on the 'Orphanage Registration Policy' document dated 24/02/2016. "
        "All answers must be based only on the policy content — do not speculate or generalize beyond the official procedures.\n\n"

        "Examples:\n"
        "Q: What documents are required to register an orphanage with NADRA?\n"
        "A: The orphanage must submit an application, its registration certificate with the Federal or Provincial Government, and a filled Orphanage Registration Form (Annex-A) with guardian details.\n\n"
        
        "Q: Who approves the registration of an orphanage in the NADRA database?\n"
        "A: The registration is approved by the Chief Operating Officer or DG (Ops) at NADRA HQ.\n\n"
        
        "Q: What is the purpose of orphan registration with NADRA?\n"
        "A: It ensures legal identity and helps safeguard orphan children’s fundamental rights like education, healthcare, and social protection.\n\n"
        
        "Q: Was this policy legally endorsed?\n"
        "A: Yes, the policy was presented before the Supreme Court of Pakistan (Human Rights Case No. 22607-S/2011) and the Lahore High Court (W.P. No. 20197/2014) and was endorsed accordingly."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

