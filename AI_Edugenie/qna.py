from gemini_client import get_gemini


SYSTEM = """You are EduGenie, a helpful educational assistant.
Answer questions accurately and clearly for learners.
Prefer concise explanations, use examples when useful, and state uncertainty when the
question cannot be answered reliably from the available information.
Do not pretend to have personal experiences or access to private data."""


async def answer_question(question: str) -> str:
    prompt = f"""Answer this learner's question.

Question:
{question}

Give a direct answer first, then a short explanation if useful."""
    return get_gemini().generate(
        prompt,
        system_instruction=SYSTEM,
        temperature=0.3,
        max_output_tokens=900,
    )
