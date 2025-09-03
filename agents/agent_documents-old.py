# # agents/agent_documents.py

import json
import os
import sys
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from model import get_llm_response  # only used in keyword extraction

# # ────────────────────────────────────────────────────────────────────────────────
# # LOAD DATASET
# # ────────────────────────────────────────────────────────────────────────────────

# def load_qa_data():
#     file_path = os.path.join("data", "qa_data_with_context.json")
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)

# QA_DATA = load_qa_data()

# # ────────────────────────────────────────────────────────────────────────────────
# # CONTEXT TAGGING (via LLM)
# # ────────────────────────────────────────────────────────────────────────────────

# def extract_context_keywords(user_query: str):
#     system_prompt = """
# You are a smart context tagger for NADRA document-related queries.
# Given a user's question, extract the key context words that best describe the intent.

# You must extract:
# - Product Type (e.g., CNIC, CRC, NICOP, Smart ID, Succession Certificate)
# - Operation Type (e.g., New, Modification, Renewal, Reprint, Office Mistake, Conversion)
# - Field (optional, e.g., Father Name, Mother Name, DOB, Gender, Religion, Marital Status)

# Important:
# - Treat "change" and "update" as equivalent to "Modification"
# - Do not invent new tags outside the predefined categories

# Format your output as a JSON list of context tags like:
# ["CNIC", "Modification", "Father Name"]
# """
#     messages = [
#         {"role": "system", "content": system_prompt.strip()},
#         {"role": "user", "content": user_query.strip()}
#     ]
#     response = get_llm_response(messages)
#     try:
#         tags = json.loads(response)
#         if isinstance(tags, list):
#             return set(tag.strip().lower() for tag in tags)
#     except:
#         pass
#     return set()
# #---------------------------------------------------------------------------------


# # ────────────────────────────────────────────────────────────────────────────────
# # Q/A MATCHING
# # ────────────────────────────────────────────────────────────────────────────────

# def match_best_answer(user_query: str):
#     query_context = extract_context_keywords(user_query)

#     if not query_context:
#         return "Sorry, I couldn't determine your request clearly. Please rephrase or contact NADRA directly."

#     best_score = 0
#     best_answer = None

#     for entry in QA_DATA:
#         entry_context = set(tag.strip().lower() for tag in entry.get("context", []))
#         score = len(query_context.intersection(entry_context))

#         if score > best_score:
#             best_score = score
#             best_answer = entry["answer"]

#     return best_answer or "Sorry, I couldn't find the exact documents for your request. Please try rephrasing or contact NADRA directly."

# # ────────────────────────────────────────────────────────────────────────────────
# # MAIN INTERFACES
# # ────────────────────────────────────────────────────────────────────────────────

# async def query_agent(user_query: str):
#     async def response_stream():
#         yield match_best_answer(user_query)
#     return {
#         "source": "qa_data_with_context.json",
#         "answer": response_stream()
#     }
# -------------------------------------------------------------------------------------------------------
# agents/agent_documents.py

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from model import get_llm_response, stream_llm_response

# ────────────────────────────────────────────────────────────────────────────────
# CONTEXT LOADING
# ────────────────────────────────────────────────────────────────────────────────

def load_qa_data():
    file_path = os.path.join("data", "qa_data_with_context.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

CONTEXT = load_qa_data()

# def load_context():
#     file_path = os.path.join("data", "documents_final.md")
#     with open(file_path, "r", encoding="utf-8") as f:
#         return f.read().strip()

# CONTEXT = load_context()

# ────────────────────────────────────────────────────────────────────────────────
# SYNC RESPONSE
# ────────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    system_prompt = f"""
        You are a smart context tagger for NADRA document-related queries.
        # Given a user's question, extract the key context words that best describe the intent.

        # You must extract:
        # - Product Type (e.g., CNIC, CRC, NICOP, Smart ID, Succession Certificate)
        # - Operation Type (e.g., New, Modification, Renewal, Reprint, Office Mistake, Conversion)
        # - Field (optional, e.g., Father Name, Mother Name, DOB, Gender, Religion, Marital Status)

        # Important:
        # - Treat "change" and "update" as equivalent to "Modification"
        # - Do not invent new tags outside the predefined categories

        # Format your output as a JSON list of context tags like:
        # ["CNIC", "Modification", "Father Name"]
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    response = get_llm_response(messages)
    print("[DEBUG] Model responded:", response)
    return {
        "source": "documents_final.md",
        "answer": response
    }

# ────────────────────────────────────────────────────────────────────────────────
# ASYNC STREAMING RESPONSE
# ────────────────────────────────────────────────────────────────────────────────

async def handle_query_stream(user_query):
    system_prompt = f"""
        You are a smart context tagger for NADRA document-related queries.
        # Given a user's question, extract the key context words that best describe the intent.

        # You must extract:
        # - Product Type (e.g., CNIC, CRC, NICOP, Smart ID, Succession Certificate)
        # - Operation Type (e.g., New, Modification, Renewal, Reprint, Office Mistake, Conversion)
        # - Field (optional, e.g., Father Name, Mother Name, DOB, Gender, Religion, Marital Status)

        # Important:
        # - Treat "change" and "update" as equivalent to "Modification"
        # - Do not invent new tags outside the predefined categories

        # Format your output as a JSON list of context tags like:
        # ["CNIC", "Modification", "Father Name"]

        Here is the official documentation context:

        {CONTEXT}


        """.strip()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk
