from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator


class ProgressUpdate(BaseModel):
    status: Literal["OPEN", "IN_PROGRESS", "DONE", "NOT_APPLICABLE"]


class ProgressOut(BaseModel):
    id: str
    checklist_item_id: str
    status: str
    updated_at: datetime
    completed_at: datetime | None
    completed_by: str | None

    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be empty")
        return v.strip()


class CommentOut(BaseModel):
    id: str
    progress_id: str
    user_id: str
    text: str
    created_at: datetime

    model_config = {"from_attributes": True}
