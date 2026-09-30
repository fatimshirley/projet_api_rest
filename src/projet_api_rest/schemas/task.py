from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
    )
    description: str | None = None
    priority: Literal["low", "medium", "high"]


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    description: str | None = None
    priority: Literal["low", "medium", "high"] | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: Literal["low", "medium", "high"]
    completed: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
