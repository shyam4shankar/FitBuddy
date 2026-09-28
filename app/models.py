<<<<<<< HEAD
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
=======
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):

    __tablename__ = "users"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )


    user_id: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        index=True,
        nullable=False,
    )


    username: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )


    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )


    goal: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )


    intensity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


    plans: Mapped[list["Plan"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Plan(Base):

    __tablename__ = "plans"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )


    user_id: Mapped[str] = mapped_column(
        String(80),
        ForeignKey(
            "users.user_id",
            ondelete="CASCADE",
        ),
        index=True,
        nullable=False,
    )


    original_plan: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )


    updated_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    nutrition_tip: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )


    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


    user: Mapped["User"] = relationship(
        back_populates="plans"
    )
>>>>>>> e41828e (Initial FitBuddy project)
