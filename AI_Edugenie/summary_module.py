from gemini_client import get_gemini


async def summarize_text(text: str) -> str:
    prompt = f"""Summarize the following educational passage.

Requirements:
- Keep the important facts and relationships.
- Remove repetition and unnecessary detail.
- Use simple language.
- Return a concise summary suitable for revision.

Passage:
{text}"""

    return get_gemini().generate(
        prompt,
        system_instruction="You are an educational summarization assistant.",
        temperature=0.2,
        max_output_tokens=900,
    )
