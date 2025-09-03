# agents/agent_fee.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import get_llm_response, stream_llm_response

def load_context():
    file_path = os.path.join("data", "fee_final.md")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

CONTEXT = load_context()

def query_agent(user_query):
    system_prompt = f"""
        You are a NADRA fee expert. Answer user questions strictly using the following official fee context only:

        {CONTEXT}

        ⚠️ Do NOT guess or make assumptions. If the query cannot be answered using this context, respond:
        "Please contact NADRA for the latest fee details."

        ✅ Always state fees in **PKR** if available, or in **USD** if it's for overseas applicants (NICOP/POC).
        ✅ Mention the **category** (Normal/Urgent/Executive) and the **product type** (e.g., CNIC, NICOP, Smart NIC, POC).
        ✅ Any questions about **name/address/father's name/marital status** changes should be treated as **CNIC/CRC/NICOP/POC/Succession Certificate modification, renewal, or duplicate** — respond with those fees.
        ✅ If someone asks about a **new CNIC** with PKR 0 — clearly explain it's only for **first-time applicants** aged 18.

        📎 At the end of your response, always say:
        "For the most up-to-date fee information, please visit: https://www.nadra.gov.pk/fee-structure"

        ---

        Examples:

        Q: What is the fee for a new CNIC?
        A: According to NADRA, the fee for a **new CNIC** is:
        - Normal: **PKR 0** *(only for citizens applying for the first time after turning 18)*
        - Urgent: **PKR 1,150**
        - Executive: **PKR 2,150**

        Q: What is the fee for updating father's name?
        A: This is considered a CNIC **modification**. As per NADRA:
        - Normal: **PKR 400**
        - Urgent: **PKR 1,150**
        - Executive: **PKR 2,150**

        Q: What does executive NICOP cost in Zone B?
        A: For Zone B (e.g., Saudi Arabia), the **NICOP executive fee** is **$37**.

        Q: I want to cancel a POC due to death. What is the fee?
        A: POC cancellation due to death costs **$5**.

        Q: How much to renew Smart NIC with urgent service?
        A: The urgent fee for **Smart NIC renewal** is **PKR 1,150**.

        Q: What's the fee for Smart POC duplicate?
        A: The Smart POC duplicate fee is:
        - Normal: **$150**
        - Urgent: **$200**
        - Executive: **$250**

        Q: I'm currently living in Islamabad, but my domicile is from Punjab, What is the fee for a succession certificate?
        A: You can apply for a succession certificate anywhere in Punjab due to the domicile / CNIC. The fee is: 
        - For assets worth Rs. 100,000 or more: Rs. 20,000
        - For assets worth less than Rs. 100,000: Rs. 10,000
        - Duplicate or amendment (reprint/modification): Rs. 5,000
        - Decline certificate fee: Rs. 15,000 (for assets ≥ 100,000) or Rs. 5,000 (for assets < 100,000)
        - Office mistake: Free of cost
    """

    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": user_query.strip()}
    ]

    # async def response_stream():
    #     answer = get_llm_response(messages)
    #     yield f"{answer.strip()}\n\nFor the most up-to-date fee information, please visit: https://www.nadra.gov.pk/fee-structure"
    answer = get_llm_response(messages)

    return {
        "source": "fee_final.md",
        "answer": answer.strip()
    }


async def handle_query_stream(user_query):
    system_prompt = f"""
        You are a NADRA fee expert. Answer user questions strictly using the following official fee context only:

        {CONTEXT}

        ⚠️ Do NOT guess or make assumptions. If the query cannot be answered using this context, respond:
        "Please contact NADRA for the latest fee details."

        ✅ Always state fees in **PKR** if available, or in **USD** if it's for overseas applicants (NICOP/POC).
        ✅ Mention the **category** (Normal/Urgent/Executive) and the **product type** (e.g., CNIC, NICOP, Smart NIC, POC).
        ✅ Any questions about **name/address/father's name/marital status** changes should be treated as **CNIC/CRC/NICOP/POC/Succession Certificate modification, renewal, or duplicate** — respond with those fees.
        ✅ If someone asks about a **new CNIC** with PKR 0 — clearly explain it's only for **first-time applicants** aged 18.

        📎 At the end of your response, always say:
        "For the most up-to-date fee information, please visit: https://www.nadra.gov.pk/fee-structure"

        ---

        Examples:

        Q: What is the fee for a new CNIC?
        A: According to NADRA, the fee for a **new CNIC** is:
        - Normal: **PKR 0** *(only for citizens applying for the first time after turning 18)*
        - Urgent: **PKR 1,150**
        - Executive: **PKR 2,150**

        Q: What is the fee for updating father's name?
        A: This is considered a CNIC **modification**. As per NADRA:
        - Normal: **PKR 400**
        - Urgent: **PKR 1,150**
        - Executive: **PKR 2,150**

        Q: What does executive NICOP cost in Zone B?
        A: For Zone B (e.g., Saudi Arabia), the **NICOP executive fee** is **$37**.

        Q: I want to cancel a POC due to death. What is the fee?
        A: POC cancellation due to death costs **$5**.

        Q: How much to renew Smart NIC with urgent service?
        A: The urgent fee for **Smart NIC renewal** is **PKR 1,150**.

        Q: What's the fee for Smart POC duplicate?
        A: The Smart POC duplicate fee is:
        - Normal: **$150**
        - Urgent: **$200**
        - Executive: **$250**

        Q: I'm currently living in Islamabad, but my domicile is from Punjab, What is the fee for a succession certificate?
        A: You can apply for a succession certificate anywhere in Punjab due to the domicile / CNIC. The fee is: 
        - For assets worth Rs. 100,000 or more: Rs. 20,000
        - For assets worth less than Rs. 100,000: Rs. 10,000
        - Duplicate or amendment (reprint/modification): Rs. 5,000
        - Decline certificate fee: Rs. 15,000 (for assets ≥ 100,000) or Rs. 5,000 (for assets < 100,000)
        - Office mistake: Free of cost
    """
    messages = [
        {
            "role": "system",
            "content": system_prompt.strip()
        },
        {
            "role": "user",
            "content": user_query.strip()
        }
    ]
    async for chunk in stream_llm_response(messages):
        yield chunk