from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Literal


class FitnessPlanRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    goal: str = Field(..., min_length=1, max_length=200)
    experience_level: Literal["beginner", "intermediate", "advanced"]
    age: int = Field(..., ge=13, le=100)
    gender: str = Field(..., min_length=1, max_length=20)
    weight_kg: float = Field(..., gt=0)
    height_cm: float = Field(..., gt=0)
    available_days_per_week: int = Field(..., ge=1, le=7)
    available_minutes_per_day: int = Field(..., ge=15, le=240)
    equipment: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)


class FitnessPlanResponse(BaseModel):
    summary: str
    weekly_plan: List[str]
    notes: List[str]
