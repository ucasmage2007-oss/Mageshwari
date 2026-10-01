from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from schemas import (
    TextRequest, QuizRequest, QAResponse, TextResponse, QuizResponse,
    ErrorResponse
)
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie - Gemini Powered Learning Assistant",
    version="1.0.0",
    description="AI-powered educational assistant with Q&A, explanations, quizzes, summaries, and learning paths.",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name,
            "gemini_configured": bool(settings.gemini_api_key),
        },
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "gemini_configured": bool(settings.gemini_api_key),
    }


@app.post("/qa", response_model=QAResponse, responses={500: {"model": ErrorResponse}})
async def qa(payload: TextRequest):
    answer = await answer_question(payload.text)
    return QAResponse(answer=answer)


@app.post("/explain", response_model=TextResponse, responses={500: {"model": ErrorResponse}})
async def explain(payload: TextRequest):
    result = await explain_concept(payload.text)
    return TextResponse(result=result)


@app.post("/quiz", response_model=QuizResponse, responses={500: {"model": ErrorResponse}})
async def quiz(payload: QuizRequest):
    questions = await generate_quiz(payload.text, payload.count)
    return QuizResponse(questions=questions)


@app.post("/summarize", response_model=TextResponse, responses={500: {"model": ErrorResponse}})
async def summarize(payload: TextRequest):
    result = await summarize_text(payload.text)
    return TextResponse(result=result)


@app.post("/learn/recommendations", response_model=TextResponse, responses={500: {"model": ErrorResponse}})
async def learn_recommendations(payload: TextRequest):
    result = await get_learning_recommendations(payload.text)
    return TextResponse(result=result)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    # Avoid exposing provider credentials or stack traces to browser users.
    return JSONResponse(
        status_code=500,
        content={"detail": "EduGenie could not complete the request. Check the server terminal for details."},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.reload)
