from gemini_client import get_gemini


async def explain_concept(topic: str) -> str:
    prompt = f"""
Explain this educational concept to a beginner:

{topic}

Use this structure:
1. Simple definition
2. Main idea
3. Important points
4. Easy example
"""
    return get_gemini().generate(
        prompt,
        system_instruction="You are EduGenie. Explain complex concepts in beginner-friendly language.",
        temperature=0.3,
        max_output_tokens=800,
    )
