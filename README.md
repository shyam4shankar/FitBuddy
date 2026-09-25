# FitBuddy

AI Fitness Plan Generator using FastAPI and Gemini.

## Overview
FitBuddy is a small FastAPI application that takes a user's fitness goals, experience level, available equipment, and schedule, then generates a personalized training plan using Google's Gemini API.

## Features
- Health check endpoint
- Personalized fitness plan generation
- Request validation with Pydantic
- Environment-based configuration

## Local setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

4. Add your Gemini API key in `.env`:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. Start the app:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Open the API docs:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Example request

```bash
curl -X POST "http://localhost:8000/generate-plan" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "goal": "Build muscle and improve strength",
    "experience_level": "beginner",
    "age": 28,
    "gender": "female",
    "weight_kg": 65,
    "height_cm": 170,
    "available_days_per_week": 4,
    "available_minutes_per_day": 45,
    "equipment": ["dumbbells", "bench"],
    "constraints": ["No jumping", "Prefer home workouts"]
  }'
```

## Environment variables

- `GEMINI_API_KEY`: your Google Gemini API key
- `GEMINI_MODEL`: the Gemini model to use (default: `gemini-1.5-flash`)
- `APP_NAME`: application name (default: `FitBuddy`)

## Notes
This is an initial project scaffold. The plan generation logic is intentionally simple and can be extended with additional training data, meal plans, recovery tracking, or user accounts.
