import json
from typing import Any

from gemini_client import get_gemini
from schemas import QuizQuestion


QUIZ_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "question": {"type": "string"},
            "options": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 4,
                "maxItems": 4,
            },
            "correct_answer": {"type": "string"},
            "explanation": {"type": "string"},
        },
        "required": ["question", "options", "correct_answer", "explanation"],
    },
}


def _validate_questions(data: Any, count: int) -> list[QuizQuestion]:
    if not isinstance(data, list):
        raise ValueError("Quiz response was not a JSON array.")

    cleaned: list[QuizQuestion] = []
    for item in data[:count]:
        if not isinstance(item, dict):
            continue

        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        correct = str(item.get("correct_answer", "")).strip()
        explanation = str(item.get("explanation", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4:
            continue
        options = [str(x).strip() for x in options]
        if any(not x for x in options) or correct not in options:
            continue

        cleaned.append(
            QuizQuestion(
                question=question,
                options=options,
                correct_answer=correct,
                explanation=explanation,
            )
        )

    if len(cleaned) != count:
        raise ValueError(
            f"Gemini returned {len(cleaned)} valid questions; expected {count}."
        )
    return cleaned


async def generate_quiz(source_text: str, count: int = 3) -> list[QuizQuestion]:
    prompt = f"""Create exactly {count} multiple-choice questions from the educational
text below.

Rules:
- Each question must be answerable from the text.
- Each question has exactly four options.
- Exactly one option is correct.
- "correct_answer" must exactly match one option.
- Include a concise explanation of the correct answer.
- Do not use markdown.

Source text:
{source_text}"""

    raw = get_gemini().generate(
        prompt,
        system_instruction=(
            "You generate reliable educational MCQs. Follow the requested JSON schema exactly."
        ),
        json_schema=QUIZ_SCHEMA,
        temperature=0.4,
        max_output_tokens=1800,
    )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("Gemini returned invalid JSON for the quiz.") from exc

    return _validate_questions(data, count)
