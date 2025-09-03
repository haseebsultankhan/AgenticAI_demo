# run.py

from controller_v1 import route_query, resolve_agent as resolve_agent_name

from prettytable import PrettyTable
import importlib
import os
import asyncio
import re

def print_location_response(response):
    rows = response.get("locations", [])
    if not rows:
        print(f"\n❌ No NADRA centers found for '{response.get('extracted_location')}'")
        return

    agent = response.get("agent", "Unknown Agent")
    print(f"\nAnswer from {agent}:")
    print(f"📍 Results for '{response['extracted_location']}' ({response['matches_found']} centers):\n")

    table = PrettyTable()
    table.field_names = ["Address", "Location", "Phone"]
    for row in rows:
        table.add_row([row["address"], row["location"], row["phone"]])

    print(table)

def expand_abbreviations(text):
    glossary_path = "data/glossary_final.md"
    if not os.path.exists(glossary_path):
        return text

    with open(glossary_path, "r", encoding="utf-8") as f:
        glossary = f.read()

    glossary_pairs = re.findall(r"\*\*(.*?)\*\* — (.*)", glossary)
    abbreviation_map = {abbr.strip(): desc.strip() for abbr, desc in glossary_pairs}

    for abbr, full in abbreviation_map.items():
        pattern = r'\b' + re.escape(abbr) + r'\b'
        replacement = f"{abbr} ({full})"
        text = re.sub(pattern, replacement, text)

    return text

async def print_streaming_response(agent_name, user_query):
    try:
        agent_module = importlib.import_module(f"agents.{agent_name}")
        handle_stream = getattr(agent_module, "handle_query_stream", None)
        if handle_stream:
            print(f"\n Answer from {agent_name}:\n", end="", flush=True)
            async for chunk in handle_stream(user_query):
                print(chunk, end="", flush=True)
            print()
        else:
            print(f"\n⚠️ Agent '{agent_name}' does not support streaming.")
    except Exception as e:
        print(f"\n❌ Error streaming from {agent_name}: {e}")

def print_response(response, user_query):
    if "error" in response:
        print(f"\n❌ Error: {response['error']}")
    elif "locations" in response:
        print_location_response(response)
    elif "output" in response:
        print(response["output"])
    elif "answer" in response:
        agent = response.get("agent", "Unknown Agent")
        if agent in ["agent_default", "agent_location", "agent_documents"]:
            print(f"\n Answer from {agent}:\n{response['answer']}")
        else:
            corrected = expand_abbreviations(response["answer"])
            print(f"\n Answer from {agent}:\n{corrected}")
    else:
        print("\n Response:")
        print(response)

async def main():
    print("💬 NADRA Agentic RAG is live. Ask anything or type 'exit'.")
    while True:
        q = input("\n👤 You: ").strip()
        if q.lower() in ("exit", "quit"):
            print("👋 Exiting.")
            break

        response = await route_query(q)
        agent = response.get("agent")

        # If streaming is supported by this agent
        if agent and agent not in ["agent_location", "agent_default", "agent_documents"]:
            await print_streaming_response(agent, q)
        else:
            print_response(response, q)

if __name__ == "__main__":
    asyncio.run(main())
