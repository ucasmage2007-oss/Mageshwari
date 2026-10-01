from gemini_client import get_gemini


async def get_learning_recommendations(topic: str) -> str:
    prompt = f"""Create a structured learning path for: {topic}

Include:
1. Prerequisites
2. Beginner topics
3. Intermediate topics
4. Advanced topics
5. A practical project or exercise at each major stage
6. Suggested learning resources by type (documentation, articles, books, videos)
7. A realistic sequence and approximate time guidance

Adapt the path for a learner who may be starting from basic knowledge."""

    return get_gemini().generate(
        prompt,
        system_instruction=(
            "You are an educational curriculum assistant. Build structured, "
            "practical learning paths without inventing specific resource URLs."
        ),
        temperature=0.5,
        max_output_tokens=1800,
    )
