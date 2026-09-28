from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import init_db
from app.routes import router


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Create FastAPI application
app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description=(
        "FitBuddy generates personalized 7-day fitness plans, "
        "nutrition tips, and AI-based plan updates."
    ),
    version="1.0.0",
)


# Serve CSS, JavaScript and other static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


# Jinja2 HTML templates
templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# Register FitBuddy routes
app.include_router(router)


# Initialize database when application starts
@app.on_event("startup")
def startup_event():
    init_db()


# Health-check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "application": "FitBuddy",
        "version": "1.0.0",
        "message": "FitBuddy is running successfully"
    }