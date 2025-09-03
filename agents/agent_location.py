# agents/agent_location.py

import os
import sys
import subprocess
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response

# === INTENT CHECK PROMPT ===
INTENT_PROMPT = """
Determine if the user's question is actually about a NADRA center or office location.

Examples:
- "Where is NADRA office in dgk?" → yes
- "Where can I get my CNIC in lahore?" → yes
- "What is the weather in islamabad?" → no
- "Tell me about traffic in karachi" → no
- "Where is office in multan?" → yes
- "nadra ka daftar kidhar hai islamabad main?" → yes

Only respond with one word: 'yes' or 'no'.
"""

# === LOCATION EXTRACTION PROMPT ===
EXTRACTION_PROMPT = """
Extract the exact city or alias keyword from this sentence. If the user used an alias like 'lhr', 'fsd', 'khi', 'dgk', return it as-is.
If the user wrote a full city name like 'lahore', 'karachi', 'dera ghazi khan', return that as-is.

⚠️ Only return a single word or phrase used by the user — don't try to expand or standardize it yourself.

Examples:
- "where is nadra office in fsd?" → fsd
- "find nadra center in lahore" → lahore
- "offices in dgk please?" → dgk
- "what’s nearest NADRA in rahim yar khan" → rahim yar khan
"""

def extract_location(user_input):
    # Step 1: Intent check
    intent_messages = [
        {"role": "system", "content": INTENT_PROMPT.strip()},
        {"role": "user", "content": user_input.strip()}
    ]
    intent = get_llm_response(intent_messages).strip().lower()

    if intent != "yes":
        from agents import agent_default
        return {
            "source": "default",
            "answer": agent_default.query_agent(user_input)["answer"]
        }

    # Step 2: Location keyword extraction
    extract_messages = [
        {"role": "system", "content": EXTRACTION_PROMPT.strip()},
        {"role": "user", "content": user_input.strip()}
    ]
    return get_llm_response(extract_messages)

def query_agent(user_query):
    try:
        extracted = extract_location(user_query)

        if isinstance(extracted, dict):
            print("🤖 [agent_location] Intent check failed, falling back.")
            return extracted

        extracted_keyword = extracted

        result = subprocess.run(
            [sys.executable, "search_loc.py"],
            input=extracted_keyword.encode("utf-8"),
            capture_output=True
        )

        raw_output = result.stdout.decode("utf-8").strip()

        if "No results found" in raw_output.lower():
            return {
                "source": "locations_cleaned.xlsx",
                "extracted_location": extracted_keyword,
                "output": f"❌ No NADRA centers found for '{extracted_keyword}'"
            }

        return {
            "source": "locations_cleaned.xlsx",
            "extracted_location": extracted_keyword,
            "output": raw_output
        }

    except subprocess.TimeoutExpired:
        return {"error": "Timeout while querying location agent."}
    except Exception as e:
        return {"error": str(e)}

# ─────────────────────────────────────────────────────────────────────────────
# Async streaming version
# ─────────────────────────────────────────────────────────────────────────────

async def handle_query_stream(user_query):
    try:
        extracted = extract_location(user_query)

        if isinstance(extracted, dict):
            yield extracted["answer"]
            return

        extracted_keyword = extracted

        process = await asyncio.create_subprocess_exec(
            sys.executable, "search_loc.py",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate(input=extracted_keyword.encode("utf-8"))

        output = stdout.decode("utf-8").strip()

        if "No results found" in output.lower():
            yield f"❌ No NADRA centers found for '{extracted_keyword}'"
        else:
            for line in output.splitlines():
                yield line

    except asyncio.TimeoutError:
        yield "⏱️ Timeout while querying location service."
    except Exception as e:
        yield f"❌ Error: {str(e)}"
