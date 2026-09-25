from __future__ import annotations

import os
from typing import Any

import google.generativeai as genai


def generate_plan_text(payload: dict[str, Any]) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "Gemini API key not configured. Set GEMINI_API_KEY in your environment "
            "or .env file to enable AI-generated plans."
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))

    prompt = f"""
    Create a personalized fitness plan for the following user.
    User profile:
    - Name: {payload.get('name', 'Athlete')}
    - Goal: {payload.get('goal', 'general fitness')}
    - Experience: {payload.get('experience_level', 'beginner')}
    - Age: {payload.get('age', 30)}
    - Gender: {payload.get('gender', 'not specified')}
    - Weight: {payload.get('weight_kg', 70)} kg
    - Height: {payload.get('height_cm', 170)} cm
    - Available days per week: {payload.get('available_days_per_week', 3)}
    - Available minutes per day: {payload.get('available_minutes_per_day', 30)}
    - Equipment: {', '.join(payload.get('equipment', [])) or 'bodyweight only'}
    - Constraints: {', '.join(payload.get('constraints', [])) or 'none'}

    Provide a concise but useful plan with:
    1. A short summary
    2. A weekly plan with 3-7 bullet points
    3. Recovery and safety notes
    """

    response = model.generate_content(prompt)
    return response.text
