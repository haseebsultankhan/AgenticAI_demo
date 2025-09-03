# agents/agent_tracking.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

def load_context():
    file_path = os.path.join("data", "processing_time_final.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

PROCESSING_CONTEXT = load_context()

# ─────────────────────────────────────────────────────────────────────────────
# Sync Response (for API/controller)
# ─────────────────────────────────────────────────────────────────────────────

def query_agent(user_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You handle tracking-related queries for NADRA services only.\n\n"
                "✅ Your response must strictly follow this structure:\n\n"
                "For tracking your application status, please contact NADRA helpline directly:\n"
                "📞 Timings: 24/7\n"
                "📱 Mobile: 1777\n"
                "• 📞 Helpline: 051-111-786-100\n"
                "• 🏢 Visit your nearest NADRA Registration Center (NRC)\n\n"
                "Here are the typical processing durations:\n"
                "- CNIC Normal: 30 days\n"
                "- CNIC Urgent: 12 days\n"
                "- CNIC Executive: 7 days\n"
                "- NICOP: 7–30 days (based on country of application)\n"
                "- FRC (online): Delivered instantly in digital format\n\n"
                "📌 Note: These are typical processing durations and do not reflect individual application timelines.\n\n"
                "NEVER:\n"
                "- Apologize\n"
                "- Say 'I'm unable to' or refer to yourself as AI\n"
                "- Predict or assume delivery or tracking status\n"
                "- Use vague language like 'please be patient'\n"
            )
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]

    return {
        "source": "processing_time_final.md",
        "answer": get_llm_response(messages)
    }

# ─────────────────────────────────────────────────────────────────────────────
# Async Streaming Response (for terminal/chat UI)
# ─────────────────────────────────────────────────────────────────────────────

from model import stream_llm_response

async def handle_query_stream(user_query):
    system_prompt = (
        "You handle tracking-related queries for NADRA services only.\n\n"
        "✅ Your response must strictly follow this structure:\n\n"
        "For tracking your application status, please contact NADRA helpline directly:\n"
        "📞 Timings: 24/7\n"
        "📱 Mobile: 1777\n"
        "• 📞 Helpline: 051-111-786-100\n"
        "• 🏢 Visit your nearest NADRA Registration Center (NRC)\n\n"
        "Here are the typical processing durations:\n"
        "- CNIC Normal: 30 days\n"
        "- CNIC Urgent: 12 days\n"
        "- CNIC Executive: 7 days\n"
        "- NICOP: 7–30 days (based on country of application)\n"
        "- FRC (online): Delivered instantly in digital format\n\n"
        "📌 Note: These are typical processing durations and do not reflect individual application timelines.\n\n"
        "NEVER:\n"
        "- Apologize\n"
        "- Say 'I'm unable to' or refer to yourself as AI\n"
        "- Predict or assume delivery or tracking status\n"
        "- Use vague language like 'please be patient'\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query.strip()}
    ]

    async for chunk in stream_llm_response(messages):
        yield chunk

