import asyncio

# Sync fallback agent response (used if streaming is unsupported)
def query_agent(user_query):
    default_text = (
        "I'm here to assist with queries related to NADRA services — including CNIC, NICOP, "
        "Succession Certificate, CRC, biometric updates, registration processes, card delivery, "
        "office locations, and official fees.\n\n"
        "It seems your question doesn't match a specific service category. If you believe your query is related "
        "to NADRA, please try rephrasing it for better assistance.\n\n"
        "If you're still unsure or need help, you can always contact NADRA directly:\n"
        "📞 Timings: 24/7\n"
        "📱 Mobile: 1777\n"
        "☎️ Landline: +92 51 111 786 100\n"
        "📧 Email: csd@nadra.gov.pk"
    )

    return {
        "source": "default",
        "answer": default_text
    }

# Optional streaming support
async def handle_query_stream(user_query):
    # default_text = (
    #     "I'm here to assist with queries related to NADRA services — including CNIC, NICOP, "
    #     "Succession Certificate, CRC, biometric updates, registration processes, card delivery, "
    #     "office locations, and official fees.\n\n"
    #     "It seems your question doesn't match a specific service category. If you believe your query is related "
    #     "to NADRA, please try rephrasing it for better assistance.\n\n"
    #     "If you're still unsure or need help, you can always contact NADRA directly:\n"
    #     "📞 Timings: 24/7\n"
    #     "📱 Mobile: 1777\n"
    #     "☎️ Landline: +92 51 111 786 100\n"
    #     "📧 Email: csd@nadra.gov.pk"
    # )
    default_text = (
        "👋 I'm here to assist with queries related to NADRA services.\n\n"
        "You can ask questions about the following chapters:\n"
        "• CNIC (New / Renew / Update)\n"
        "• NICOP (Overseas ID)\n"
        "• Child Registration Certificate (CRC / B-form)\n"
        "• Succession Certificate\n"
        "• Biometric updates or corrections\n"
        "• Registration procedures and documentation\n"
        "• NADRA office locations and contact details\n"
        "• Official processing fees\n"
        "• Card delivery status or issues\n"
        "• Arms Licence (registration / Renewal / Licence Procedure) \n\n"
        "📞 Need help? You can also contact NADRA directly:\n"
        "• Timings: 24/7\n"
        "• Mobile: 1777\n"
        "• Landline: +92 51 111 786 100\n"
        "• Email: csd@nadra.gov.pk"
    )

    for chunk in default_text.split("\n\n"):
        yield chunk + "\n\n"
        await asyncio.sleep(0.1)