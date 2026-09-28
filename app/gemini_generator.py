from app.config import GEMINI_WORKOUT_MODEL
from app.gemini_client import generate_text


def _demo_plan(
    name: str,
    goal: str,
    intensity: str,
) -> str:

    return f"""
FITBUDDY 7-DAY DEMO PLAN

Name: {name}

Goal: {goal.title()}

Intensity: {intensity.title()}


Important:

This is a demonstration wellness plan,
not medical advice.

Adjust activity to your comfort and ability.


DAY 1 - FULL BODY

Warm-up:
5-10 minutes of easy movement.

Main workout:
- Bodyweight squat: 2-3 sets
- Wall or incline push-up: 2-3 sets
- Glute bridge: 2-3 sets
- Easy walking: 10-15 minutes

Cool-down:
Gentle mobility and relaxed breathing.


DAY 2 - CARDIO + MOBILITY

Warm-up:
5 minutes easy walking.

Main workout:
Comfortable brisk walking or similar
moderate activity for 20-30 minutes.

Cool-down:
Gentle full-body mobility.


DAY 3 - UPPER BODY + CORE

Warm-up:
5-10 minutes.

Main workout:
- Wall/incline push-up: 2-3 sets
- Resistance-band/light row: 2-3 sets
- Dead bug: 2 sets
- Easy plank variation: 2 sets

Cool-down:
Gentle stretching.


DAY 4 - RECOVERY

Easy walking and comfortable mobility.

Keep this day light.


DAY 5 - LOWER BODY

Warm-up:
5-10 minutes.

Main workout:
- Bodyweight squat: 2-3 sets
- Supported split squat: 2 sets
- Glute bridge: 2-3 sets
- Calf raise: 2 sets

Cool-down:
Gentle mobility.


DAY 6 - ENJOYABLE CARDIO

Choose a comfortable activity such as:

- Walking
- Cycling
- Swimming
- A familiar sport

Keep the effort manageable.


DAY 7 - REST + MOBILITY

Rest.

Hydrate normally.

Sleep well.

Gentle mobility is optional if comfortable.
"""


def generate_workout_gemini(
    name: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:

    prompt = f"""
You are FitBuddy,
an AI wellness-planning assistant.

Create a practical 7-day beginner-friendly
activity plan.

User information:

Name: {name}

Age: {age}

Weight: {weight} kg

Goal: {goal}

Preferred intensity: {intensity}


Return exactly seven labeled days.

For each day include:

- Focus
- Warm-up
- Main activity
- Sets/reps OR duration
- Cool-down/recovery


Safety requirements:

- Do not diagnose medical conditions.
- Do not treat medical conditions.
- Do not prescribe medication.
- Do not prescribe supplements.
- Do not recommend extreme exercise.
- Do not recommend dangerous challenges.
- Do not recommend starvation.
- Do not recommend purging.
- Do not encourage restrictive eating.
- Do not give calorie targets.
- Avoid body-shaming language.
- Include recovery/rest.
- Keep activity appropriate to the stated intensity.
- If pain, dizziness, breathing difficulty, or another concerning symptom occurs, recommend stopping and seeking appropriate professional help.
- For minors, focus on healthy movement, enjoyment, recovery and general wellness rather than weight manipulation.
- Clearly state that this is general wellness information, not medical advice.

Keep the answer structured and easy to read.
"""


    try:

        return generate_text(
            GEMINI_WORKOUT_MODEL,
            prompt,
        )

    except Exception:

        return _demo_plan(
            name,
            goal,
            intensity,
        )