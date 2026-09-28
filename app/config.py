<<<<<<< HEAD
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from typing import Any
=======
import os
from pathlib import Path
>>>>>>> e41828e (Initial FitBuddy project)

from dotenv import load_dotenv


<<<<<<< HEAD
load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "FitBuddy")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
=======
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


APP_NAME = "FitBuddy"


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'fitbuddy.db'}",
)


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    "",
).strip()


# These can be changed inside .env.
GEMINI_WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-3.1-pro-preview",
)


GEMINI_TIP_MODEL = os.getenv(
    "GEMINI_TIP_MODEL",
    "gemini-3.8-flash",
)


AI_TIMEOUT_SECONDS = int(
    os.getenv(
        "AI_TIMEOUT_SECONDS",
        "60",
    )
)
>>>>>>> e41828e (Initial FitBuddy project)
