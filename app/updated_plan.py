from app.config import GEMINI_WORKOUT_MODEL
from app.gemini_client import generate_text


def _fallback_update(
    original_plan: str,
    feedback: str,
) -> str:

    return f"""
UPDATED FITBUDDY PLAN


Requested feedback:

{feedback}


The original plan is retained below.

In demo mode, no AI rewrite was available,
so use the feedback as a checklist and make
only comfortable, gradual changes.


ORIGINAL PLAN

{original_plan}


Safety reminder:

Stop an activity if it causes pain,
dizziness, or breathing difficulty and
seek appropriate help.
"""


def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str,
    age: int,
) -> str:

    prompt = f"""
You are updating a FitBuddy 7-day
wellness plan.


Goal:
{goal}


Preferred intensity:
{intensity}


Age:
{age}


ORIGINAL PLAN:

---START ORIGINAL---

{original_plan}

---END ORIGINAL---


USER FEEDBACK:

---START FEEDBACK---

{feedback}

---END FEEDBACK---


Create a revised seven-day plan that
incorporates reasonable feedback while
preserving recovery and safety.


Rules:

- Keep seven clearly labeled days.
- Do not recommend dangerous challenges.
- Do not recommend extreme exercise.
- Do not recommend restrictive eating.
- Do not recommend fasting.
- Do not recommend supplements.
- Do not recommend medication.
- Do not diagnose conditions.
- For minors, do not target weight loss
  or weight gain.
- Focus on healthy movement, enjoyment,
  recovery and general wellness.
- Include warm-up.
- Include cool-down/recovery.
- If feedback requests something unsafe,
  replace it with a safer alternative.
- Mention that this is general wellness
  information, not medical advice.
"""


    try:

        return generate_text(
            GEMINI_WORKOUT_MODEL,
            prompt,
        )

    except Exception:

        return _fallback_update(
            original_plan,
            feedback,
        )