from functools import lru_cache

from google import genai

from app.config import GEMINI_API_KEY


@lru_cache(maxsize=1)
def get_client():

    if not GEMINI_API_KEY:

        return None


    return genai.Client(
        api_key=GEMINI_API_KEY
    )


def generate_text(
    model: str,
    prompt: str,
) -> str:

    client = get_client()


    if client is None:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )


    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )


    text = getattr(
        response,
        "text",
        None,
    )


    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    return text.strip()