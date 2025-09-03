# agents/agent_documents.py

import json
import os
import sys
import re
from typing import Iterable

# Ensure project-root imports work when running from different CWDs
AGENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(AGENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from model import get_llm_response, stream_llm_response  # LLM only used for tag extraction


# ────────────────────────────────────────────────────────────────────────────────
# LOAD DATASET (same behavior as old code)
# ────────────────────────────────────────────────────────────────────────────────
def load_qa_data():
    file_path = os.path.join(PROJECT_ROOT, "data", "qa_data_with_context.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

QA_DATA = load_qa_data()


# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT TAGGING (same logic/contract as old code)
# ────────────────────────────────────────────────────────────────────────────────
def extract_context_keywords(user_query: str):
    system_prompt = """
You are a smart context tagger for NADRA document-related queries.
Given a user's question, extract the key context words that best describe the intent.

You must extract:
- Product Type (e.g., CNIC, CRC, NICOP, Smart ID, Succession Certificate)
- Operation Type (e.g., New, Modification, Renewal, Reprint, Office Mistake, Conversion)
- Field (optional, e.g., Father Name, Mother Name, DOB, Gender, Religion, Marital Status)

Important:
- Treat "change" and "update" as equivalent to "Modification"
- Do not invent new tags outside the predefined categories

Format your output as a JSON list of context tags like:
["CNIC", "Modification", "Father Name"]

Examples:
Q: What documents do I need to change my father's name on my NICOP?
A: ["NICOP", "Modification", "Father Name"]

Q: I want to apply for a new Smart ID. What should I bring?
A: ["Smart ID", "New"]

Q: Reprint of CRC needed. What are the documents?
A: ["CRC", "Reprint"]
"""
    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": user_query.strip()}
    ]
    response = get_llm_response(messages)

    # Be liberal in what we accept, but return a set of lowercased tags like old code
    try:
        tags = json.loads(response)
        if isinstance(tags, list):
            return set(tag.strip().lower() for tag in tags)
    except Exception:
        # Try to salvage a JSON array if the model wrapped it in text
        m = re.search(r"\[[^\]]*\]", response.strip(), flags=re.S)
        if m:
            try:
                tags = json.loads(m.group(0))
                if isinstance(tags, list):
                    return set(tag.strip().lower() for tag in tags)
            except Exception:
                pass

    return set()


# ────────────────────────────────────────────────────────────────────────────────
# Q/A MATCHING (exactly like old behavior)
# ────────────────────────────────────────────────────────────────────────────────
def match_best_answer(user_query: str):
    query_context = extract_context_keywords(user_query)

    if not query_context:
        return "Sorry, I couldn't determine your request clearly. Please rephrase or contact NADRA directly."

    best_score = 0
    best_answer = None

    for entry in QA_DATA:
        entry_context = set(tag.strip().lower() for tag in entry.get("context", []))
        score = len(query_context.intersection(entry_context))

        if score > best_score:
            best_score = score
            best_answer = entry.get("answer")

    if best_answer:
        return best_answer
    else:
        return "Sorry, I couldn't find the exact documents for your request. Please try rephrasing or contact NADRA directly."


# ────────────────────────────────────────────────────────────────────────────────
# SYNC RESPONSE (same function name & return shape as old code)
# ────────────────────────────────────────────────────────────────────────────────
def query_agent(user_query: str):
    return {
        "source": "qa_data_with_context.json",
        "answer": match_best_answer(user_query)
    }


# ────────────────────────────────────────────────────────────────────────────────
# ASYNC STREAMING RESPONSE (kept the same function name you added)
# Streams the same dataset-derived answer in chunks for your UI.
# ────────────────────────────────────────────────────────────────────────────────
async def handle_query_stream(user_query: str):
    answer = match_best_answer(user_query)
    # Stream in ~200-char chunks so the controller/UI can render progressively
    chunk_size = 200
    for i in range(0, len(answer), chunk_size):
        yield answer[i:i + chunk_size]
