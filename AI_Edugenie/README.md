# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS educational assistant based on the supplied project specification.

## Features

- Question answering (`POST /qa`)
- Beginner-friendly concept explanation (`POST /explain`)
- MCQ quiz generation (`POST /quiz`)
- Educational summarization (`POST /summarize`)
- Structured learning paths (`POST /learn/recommendations`)
- Interactive browser UI
- Health endpoint (`GET /health`)
- Optional local LaMini-Flan-T5-783M explanation model

## Architecture

Browser
  -> FastAPI
     -> Q&A / Explanation / Quiz / Summary / Learning Path modules
        -> Google Gemini API
        -> optional local LaMini-Flan-T5 model

The supplied document specifies FastAPI, an HTML/CSS frontend, Gemini for Q&A/quiz/summarization/learning paths, and LaMini-Flan-T5-783M for explanations. This implementation preserves those functional boundaries while using the current Google GenAI Python SDK.

## 1. Install Python

Use Python 3.10+ on Windows. During installation, enable **Add Python to PATH**.

Verify:

```powershell
py --version
python --version
```

If `python` is not found but `py` works, use `py` for the virtual-environment command.

## 2. Open the project in VS Code

Open the `EduGenie` folder.

Then open **Terminal -> New Terminal**.

## 3. Create a virtual environment

PowerShell:

```powershell
py -3 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this only for the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

You should now see `(.venv)` in the terminal.

## 4. Install dependencies

For the simplest Gemini-first setup:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-core.txt
```

The full `requirements.txt` also installs PyTorch/Transformers so the optional local LaMini model is available.

If you want the local explanation model:

```powershell
python -m pip install -r requirements.txt
```

## 5. Configure Gemini

Create `.env` from `.env.example`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and set:

```text
GEMINI_API_KEY=your_actual_key
```

Create the key in Google AI Studio. Do not commit `.env` to Git.

## 6. Run the application

With `(.venv)` active:

```powershell
python -m uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI API documentation is also available at:

```text
http://127.0.0.1:8000/docs
```

## 7. Test the application

Run automated tests:

```powershell
python -m pytest -q
```

Manual UI tests:

1. Ask a question: `Which is the largest ocean?`
2. Explain a concept: `Pythagorean theorem`
3. Generate a quiz from a paragraph.
4. Summarize a long educational passage.
5. Request a learning path for `SQL`.

## 8. Test the API directly

Q&A:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/qa `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Which is the largest ocean?"}'
```

Quiz:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/quiz `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"The Earth has one natural satellite called the Moon.","count":3}'
```

Summary:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/summarize `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"text":"Paste a long educational paragraph here."}'
```

## 9. Local LaMini explanation mode

The specification identifies `MBZUAI/LaMini-Flan-T5-783M` as the local explanation model.

Set:

```text
USE_LOCAL_EXPLANATION=true
```

The first explanation request can take longer because Transformers downloads the model. CPU inference can also be slower and memory-intensive.

For a lightweight laptop/desktop setup, leave it as:

```text
USE_LOCAL_EXPLANATION=false
```

Then Gemini handles `/explain` while the API and feature boundary remain the same.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── schemas.py
├── gemini_client.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-core.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_api.py
```

## Troubleshooting

### `python was not found`

Install Python 3.10+ and enable **Add Python to PATH**. Close and reopen VS Code afterward.

If `py --version` works but `python --version` does not, use:

```powershell
py -3 -m venv .venv
```

then activate the environment and use `python` from the activated environment.

### `Activate.ps1 cannot be loaded`

Use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### `GEMINI_API_KEY is not configured`

Confirm `.env` exists in the same directory as `main.py` and contains a valid key.

### Gemini model error

Change `GEMINI_MODEL` in `.env` to a text model available to your Gemini API account.

### Port 8000 is already in use

Run:

```powershell
python -m uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

### The local model is slow

Set:

```text
USE_LOCAL_EXPLANATION=false
```

Restart Uvicorn. The app will use Gemini for explanations.

## Security notes

- Never place the Gemini API key in HTML or JavaScript.
- Never commit `.env`.
- The browser calls your FastAPI backend; the backend calls Gemini.
- For production deployment, add authentication, rate limiting, request logging with secrets removed, HTTPS, and a persistent user/progress store.
