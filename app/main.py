<<<<<<< HEAD
from __future__ import annotations

from typing import List

from fastapi import FastAPI, HTTPException

from app.config import get_settings
from app.models import FitnessPlanRequest, FitnessPlanResponse
from app.services import generate_plan_text

app = FastAPI(title=get_settings().app_name, version="0.1.0")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "app": get_settings().app_name}


@app.post("/generate-plan", response_model=FitnessPlanResponse)
def generate_plan(payload: FitnessPlanRequest) -> FitnessPlanResponse:
    generated_text = generate_plan_text(payload.model_dump())

    if "Gemini API key not configured" in generated_text:
        raise HTTPException(status_code=500, detail=generated_text)

    summary = "AI-generated plan ready."
    weekly_plan: List[str] = []
    notes: List[str] = []

    lines = [line.strip() for line in generated_text.splitlines() if line.strip()]
    for line in lines:
        if line.startswith("- "):
            item = line[2:].strip()
            if not summary or summary == "AI-generated plan ready.":
                summary = item
            else:
                weekly_plan.append(item)
        elif line.lower().startswith("summary") or line.lower().startswith("overview"):
            summary = line.split(":", 1)[1].strip() if ":" in line else line
        elif line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            continue
        elif line:
            notes.append(line)

    if not weekly_plan:
        weekly_plan = [
            "Monday: Strength-focused workout with compound movements.",
            "Tuesday: Recovery walk or mobility session.",
            "Wednesday: Upper-body or lower-body workout depending on goal.",
            "Thursday: Active recovery and stretching.",
            "Friday: Conditioning or hypertrophy session.",
            "Saturday: Optional light cardio or mobility routine.",
            "Sunday: Rest and recovery.",
        ]

    if not notes:
        notes = [
            "Start with a proper warm-up before each session.",
            "Increase weights or difficulty gradually to avoid overuse injuries.",
            "Stay hydrated and prioritize sleep and recovery.",
        ]

    return FitnessPlanResponse(summary=summary, weekly_plan=weekly_plan[:7], notes=notes[:5])
=======
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import init_db
from app.routes import router


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description=(
        "AI-assisted 7-day workout and wellness planning "
        "with Gemini, FastAPI, Jinja2 and SQLite."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


templates = Jinja2Templates(
    directory=TEMPLATES_DIR
)


app.include_router(router)
>>>>>>> e41828e (Initial FitBuddy project)
