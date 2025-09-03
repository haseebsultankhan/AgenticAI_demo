# agents/agent_punjab_arms_license.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

def load_context():
    file_path = os.path.join("data", "punjab_arms_liscense.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

# ─────────────────────────────────────────────────────────────────────────────
# Sync Response (for controller.py / API calls)
# ─────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a NADRA assistant answering questions strictly based on the 'Punjab Arms Rules 2023' as issued by the Government of Punjab. "
                "Only provide information that is explicitly mentioned in the official notification. Do not speculate or interpret beyond the rules.\n\n"

                "Examples:\n"
                "Q: Who is an authorized officer for issuing arms licenses?\n"
                "A: The Additional Chief Secretary, Government of the Punjab, Home Department, or any other officer notified for the purpose is considered the authorized officer.\n\n"
                
                "Q: What is the meaning of 'business arms licence'?\n"
                "A: A business arms licence refers to a licence granted to dealers, repairers, and manufacturers of arms.\n\n"
                
                "Q: Who is eligible to inherit an arms license?\n"
                "A: A legal heir entitled by a succession certificate or NADRA-issued Family Registration Certificate can inherit a personal or business arms licence (NPB).\n\n"
                
                "Q: Where are application forms available?\n"
                "A: The application forms are available online on the official web portal of the Punjab Home Department as listed in Schedule-I."
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    return {
        "source": "punjab_arms_liscense.md",
        "answer": get_llm_response(messages)
    }

# ─────────────────────────────────────────────────────────────────────────────
# Streaming Response (for real-time display)
# ─────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You are a NADRA assistant answering questions strictly based on the 'Punjab Arms Rules 2023' as issued by the Government of Punjab. "
        "Only provide information that is explicitly mentioned in the official notification. Do not speculate or interpret beyond the rules.\n\n"

        "Examples:\n"
        "Q: Who is an authorized officer for issuing arms licenses?\n"
        "A: The Additional Chief Secretary, Government of the Punjab, Home Department, or any other officer notified for the purpose is considered the authorized officer.\n\n"
        
        "Q: What is the meaning of 'business arms licence'?\n"
        "A: A business arms licence refers to a licence granted to dealers, repairers, and manufacturers of arms.\n\n"
        
        "Q: Who is eligible to inherit an arms license?\n"
        "A: A legal heir entitled by a succession certificate or NADRA-issued Family Registration Certificate can inherit a personal or business arms licence (NPB).\n\n"
        
        "Q: Where are application forms available?\n"
        "A: The application forms are available online on the official web portal of the Punjab Home Department as listed in Schedule-I."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

