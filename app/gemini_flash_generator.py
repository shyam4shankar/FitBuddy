from app.config import GEMINI_TIP_MODEL
from app.gemini_client import generate_text


def _demo_tip(goal: str) -> str:

    tips = {

        "weight loss":
            "Focus on regular balanced meals, "
            "water, sleep, and enjoyable activity. "
            "Avoid restrictive dieting.",


        "muscle gain":
            "Include regular balanced meals with "
            "protein-rich foods such as beans, eggs, "
            "dairy, fish, or lean meats if they fit "
            "your diet.",


        "general wellness":
            "Support your routine with regular meals, "
            "hydration, sleep, enjoyable movement, "
            "and recovery.",


        "flexibility":
            "Stay hydrated, eat balanced meals, "
            "sleep well, and use gentle mobility "
            "work consistently.",
    }


    return tips.get(
        goal,
        "Aim for balanced meals, hydration, "
        "sleep, and regular enjoyable movement.",
    )


def generate_nutrition_tip_with_flash(
    goal: str,
    age: int,
) -> str:

    prompt = f"""
You are FitBuddy's nutrition and recovery
tip assistant.

Goal: {goal}

Age: {age}


Give one concise and practical wellness tip
that complements a workout plan.


Rules:

- No calorie counting.
- No restrictive diets.
- No fasting.
- No purging.
- No supplements.
- No medication recommendations.
- Do not diagnose conditions.
- For minors, emphasize balanced nutrition,
  hydration, sleep, recovery and normal growth.
- Keep it to 2-4 sentences.
- State that it is general information,
  not medical advice.
"""


    try:

        return generate_text(
            GEMINI_TIP_MODEL,
            prompt,
        )

    except Exception:

        return _demo_tip(goal)