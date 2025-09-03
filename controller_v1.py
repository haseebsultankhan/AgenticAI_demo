import importlib
from model import get_llm_response

AGENT_NAMES = {
    # Core NADRA services
    "agent_applicant_rights": "Explains the rights of NADRA applicants including privacy, fair treatment, and grievance redressal.",
    "agent_biometric_update": "Guides users on updating biometric information such as fingerprints or photos in NADRA records.",
    "agent_cards_process_workflow": "Describes step-by-step workflow for processing any NADRA card — from application to issuance.",
    "agent_chairman": "Covers questions related to NADRA’s Chairman, leadership roles, public statements, or organizational authority and his appointment date which is 2nd October 2023/",
    "agent_change_in_card": "Handles changes in CNIC details like name, address, gender, marital status, etc.",
    "agent_communication": "Describes NADRA's communication channels, complaint registration methods, escalation paths, and helplines.",
    "agent_complex_cases": "Handles special scenarios like applicants with disabilities, rare documentation, or disputed identities.",
    "agent_delivery": "Explains how NADRA delivers documents — by post, courier, or in-person — and timelines involved.",
    "agent_eligibility": "Determines who is eligible for NADRA services such as CNIC, NICOP, FRC, CRC, POC, etc.",
    "agent_fee": "Answers queries about service fees, urgent charges, executive service pricing across CNIC/NICOP/POC/etc.",
    "agent_glossary": "Provides definitions and explanations for acronyms and terms commonly used in NADRA processes.",
    "agent_lost_id_card": "Handles issues related to lost, stolen, misplaced CNICs and steps for re-issuance.",
    "agent_online_services": "Covers NADRA’s digital services including the Pak-ID portal, mobile apps, and online payments.",
    "agent_processing_time": "Details the typical processing time for different services: Normal, Urgent, and Executive.",
    "agent_products": "Outlines NADRA’s product line: Smart CNIC, NICOP, CRC, POC, FRC, etc. and their use cases.",
    "agent_registration": "Explains end-to-end registration process for CNIC, NICOP, CRC, Succession Certificates, including document verification and biometrics.",
    "agent_sms_short_codes": "Clarifies the purpose and usage of NADRA’s SMS codes: 8009, 8400, 7000, etc.",
    "agent_validity": "Provides validity period for NADRA documents and renewal criteria.",
    "agent_location": "Answers questions about where to find NADRA centers based on city or nickname (e.g., 'khi', 'lhr').",
    "agent_tracking": "Tracks the status of applied-for documents using SMS, tracking ID, or online methods.",
    "agent_documents": "Explains what documents are required for various NADRA services including first-time applications and modifications.",
    "agent_renewal": "Clarifies when and how to renew NADRA documents, and what triggers the renewal requirement.",

    # Fallback
    "agent_default": "Fallback agent for general, out-of-scope, or ambiguous questions not matched to a specific service.",

    # New/Expanded Agents
    "agent_alien_registeration": "Provides information about Alien Registration Cards (ARC), eligibility of foreigners (legal/illegal), required documents, and NADRA policy for long-term undocumented migrants.",
    "agent_arms_license": "Explains arms licensing under Pakistan Arms Rules, 2023 (Federal) — including eligibility, non-prohibited bore, antique weapons, and inheritance rules.",
    "agent_balochistan_license": "Specifically handles provincial arms license queries under Balochistan Arms Rules 2022 — such as monthly quotas and special institutional permits.",
    "agent_data_entry_operator": "Covers NADRA Data Entry Operators’ (DEOs) roles, probation, login procedures, software guidance, and policy compliance.",
    "agent_orphange": "Provides guidance on orphanage and shelter registration with NADRA, including CPI (Child Protection Information) registration protocols.",
    "agent_punjab_arms": "Handles licensing queries under Punjab Arms Rules 2023 — including business licenses, process flow, and issuing authorities.",
    "agent_succession_certificate": "Details the legal and procedural framework of Succession Certificates, SFU (Succession Facilitation Units), heirship validation, and factual controversies.",
    "agent_transgender": "Guides transgender applicants on NADRA’s inclusion policies, committee verification, Supreme Court rulings, and gender-sensitive procedures.",
    "agent_nadra_ordinance": "Provides authoritative answers based on the NADRA Ordinance 2000, including legal powers, duties, structure, and specific sections."
}

ROUTING_SYSTEM_PROMPT = """
You are a routing assistant. Your job is to choose the best agent from the list below to handle a user's question.
Return only the exact agent name (e.g., agent_fee, agent_location) — nothing else.
Here are the available agents:
""" + "\n".join([f"- {k}: {v}" for k, v in AGENT_NAMES.items()]) + """

Here are example queries and their correct agent mappings:

# agent_alien_registeration
- "Can a foreigner staying illegally for 5 years register with NADRA?" -> agent_alien_registeration
- "Mere paas visa expire hogaya hai, ARC ban sakta hai?" -> agent_alien_registeration
- "5 saal se reh raha hoon bina documents ke, registration ho sakti hai?" -> agent_alien_registeration
- "Documents required for Alien Registration Card?" -> agent_alien_registeration

# agent_arms_license
- "What is a non-prohibited bore weapon?" -> agent_arms_license
- "Who is a legal heir for arms license?" -> agent_arms_license
- "Mujhe arms license transfer karwana hai, legal heir kaun hoga?" -> agent_arms_license
- "Antique weapon ka license ban sakta hai?" -> agent_arms_license
- "Pakistan mein arms license ka process kya hai?" -> agent_arms_license

# agent_balochistan_license
- "Monthly quota for arms licenses in Balochistan?" -> agent_balochistan_license
- "Institute ko arms license kaisay milta hai?" -> agent_balochistan_license
- "Gratis license limit Balochistan arms rules?" -> agent_balochistan_license
- "Provincial license Balochistan mein kaise milta hai?" -> agent_balochistan_license

# agent_punjab_arms
- "Who issues arms licenses in Punjab?" -> agent_punjab_arms
- "Punjab mein arms license kaise milta hai?" -> agent_punjab_arms
- "Business arms license Punjab rules?" -> agent_punjab_arms
- "Punjab mein arms license kahan apply karein?" -> agent_punjab_arms

# agent_data_entry_operator
- "What is the probation period for DEO?" -> agent_data_entry_operator
- "How does a DEO log in?" -> agent_data_entry_operator
- "DEO ko login karne ke liye kya steps hain?" -> agent_data_entry_operator
- "Checklist to avoid DEO rejection?" -> agent_data_entry_operator

# agent_orphange
- "How can an orphanage register with NADRA?" -> agent_orphange
- "CPI form kahan se milega?" -> agent_orphange
- "HQ NADRA approval for orphanage?" -> agent_orphange
- "What documents are needed for orphanage registration?" -> agent_orphange

# agent_succession_certificate
- "What is SFU and what does it do?" -> agent_succession_certificate
- "SFU ka kya kaam hai succession ke case mein?" -> agent_succession_certificate
- "Factual controversy in succession certificate?" -> agent_succession_certificate
- "Succession certificate mein legal heirs kaise prove hote hain?" -> agent_succession_certificate

# agent_transgender
- "Transgender CNIC committee ka kaam kya hai?" -> agent_transgender
- "Supreme Court judgment for transgender CNIC?" -> agent_transgender
- "District committee transgender ke liye kya karti hai?" -> agent_transgender
- "Transgender registration ka process kya hai?" -> agent_transgender

# agent_nadra_ordinance
- "Section 18 of NADRA Ordinance?" -> agent_nadra_ordinance
- "NADRA kis section ke tehat CNIC cancel kar sakta hai?" -> agent_nadra_ordinance
- "What is Section 21 of the NADRA Ordinance?" -> agent_nadra_ordinance
- "NADRA ke functions kaunse ordinance mein diye gaye hain?" -> agent_nadra_ordinance

# agent_nadra_chairman
- "Who is the chairman of NADRA?" -> agent_chairman
- "NADRA ka chairman kon hai?" -> agent_chairman
- "When was the chairman appointed?" -> agent_chairman



Only return one of the agent names (e.g., `agent_fee`, `agent_documents`) — no extra text.
"""

# ────────────────────────────────────────────────────────────────────────────────
# LANGUAGE DETECTION + ENGLISH ENFORCEMENT
# ────────────────────────────────────────────────────────────────────────────────

def detect_and_translate_to_english(text: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "Detect the language of the user input. If it is not in English (e.g., Urdu or Roman Urdu), translate it to English. If it is already in English, return it unchanged. Return only the English version without explanation."
        },
        {"role": "user", "content": text.strip()}
    ]
    translated = get_llm_response(messages)
    return translated.strip()

def ensure_response_in_english(text: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "Ensure the following content is in English. If it is in another language (e.g., Urdu/Hindi), translate it. If it's already in English, return it as is. Return only the English version without explanation."
        },
        {"role": "user", "content": text.strip()}
    ]
    translated = get_llm_response(messages)
    return translated.strip()

# ────────────────────────────────────────────────────────────────────────────────
# AGENT RESOLUTION
# ────────────────────────────────────────────────────────────────────────────────

def resolve_agent(user_query: str) -> str:
    messages = [
        {"role": "system", "content": ROUTING_SYSTEM_PROMPT.strip()},
        {"role": "user", "content": user_query.strip()}
    ]
    response = get_llm_response(messages)
    return response.strip()

# ────────────────────────────────────────────────────────────────────────────────
# STREAMING ROUTER FUNCTION
# ────────────────────────────────────────────────────────────────────────────────

async def route_query_stream(user_query: str):
    try:
        translated_query = detect_and_translate_to_english(user_query)
        agent_name = resolve_agent(translated_query)
        if agent_name not in AGENT_NAMES:
            agent_name = "agent_default"

        import sys, os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        agent_module = importlib.import_module(f"agents.{agent_name}")

        # Call agent's streaming method if available
        if hasattr(agent_module, "handle_query_stream"):
            async for chunk in agent_module.handle_query_stream(user_query):
                yield chunk
        elif hasattr(agent_module, "query_agent"):
            response = agent_module.query_agent(user_query)
            if isinstance(response, dict):
                if "answer" in response:
                    yield ensure_response_in_english(response["answer"])
                elif "output" in response:
                    yield ensure_response_in_english(response["output"])
                else:
                    yield ensure_response_in_english(str(response))
            else:
                yield ensure_response_in_english(str(response))
        else:
            yield "[Error] Agent doesn't support query_agent or handle_query_stream."

    except Exception as e:
        yield f"[Error] {str(e)}"


# Add this at the end of controller_v1.py

async def route_query(user_query: str):
    chunks = []
    async for chunk in route_query_stream(user_query):
        chunks.append(chunk)
    return {
        "answer": "".join(chunks),
        "agent": resolve_agent(user_query)
    }

