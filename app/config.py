from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from typing import Any

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "FitBuddy")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
