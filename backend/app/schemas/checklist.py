from datetime import datetime

from pydantic import BaseModel


class AreaOut(BaseModel):
    id: str
    slug: str
    name: str
    emoji: str | None
    sort_order: int
    total_items: int
    done: int
    in_progress: int
    not_applicable: int

    model_config = {"from_attributes": True}


class MeasureRef(BaseModel):
    control_id: str
    parent_control_id: str | None
    group_id: str
    group_title: str
    subgroup_id: str
    subgroup_title: str
    title: str
    requirement_text: str
    guidance_text: str | None
    sec_level: str
    effort_level: int

    model_config = {"from_attributes": True}


class ChecklistItemOut(BaseModel):
    id: str
    short_description: str | None
    confidence: float
    priority: int | None
    area_slug: str
    area_name: str
    measure: MeasureRef
    # progress state for the current user's company
    status: str          # OPEN | IN_PROGRESS | DONE | NOT_APPLICABLE
    progress_id: str | None
    updated_at: datetime | None
    comment_count: int

    model_config = {"from_attributes": True}
