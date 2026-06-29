from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.auth.deps import get_verified_user
from app.database import get_db
from app.models.bsi import Area, BsiVersion, ChecklistItem, Mapping, Measure
from app.models.progress import Comment, Progress
from app.models.user import User
from app.schemas.checklist import AreaOut, ChecklistItemOut, MeasureRef

router = APIRouter(prefix="/api/v1", tags=["checklist"])

Db   = Annotated[Session, Depends(get_db)]
Auth = Annotated[User, Depends(get_verified_user)]


def _active_version(db: Session) -> BsiVersion | None:
    v = db.query(BsiVersion).filter_by(status="published").order_by(BsiVersion.created_at.desc()).first()
    return v or db.query(BsiVersion).order_by(BsiVersion.created_at.desc()).first()


def _progress_counts(db: Session, area_id: str, company_id: str) -> dict:
    rows = (
        db.query(Progress.status, func.count())
        .join(ChecklistItem, ChecklistItem.id == Progress.checklist_item_id)
        .join(Mapping, Mapping.id == ChecklistItem.mapping_id)
        .filter(Mapping.area_id == area_id)
        .filter(Progress.company_id == company_id)
        .filter(ChecklistItem.is_active == True)
        .group_by(Progress.status)
        .all()
    )
    return {status: count for status, count in rows}


@router.get("/areas", response_model=list[AreaOut])
def list_areas(db: Db, current_user: Auth):
    version = _active_version(db)
    areas = db.query(Area).order_by(Area.sort_order).all()
    result = []
    for area in areas:
        total = (
            db.query(func.count(ChecklistItem.id))
            .join(Mapping, Mapping.id == ChecklistItem.mapping_id)
            .filter(Mapping.area_id == area.id)
            .filter(ChecklistItem.is_active == True)
            .scalar() or 0
        )
        counts = _progress_counts(db, area.id, current_user.company_id)
        result.append(AreaOut(
            id=area.id,
            slug=area.slug,
            name=area.name,
            emoji=area.emoji,
            sort_order=area.sort_order,
            total_items=total,
            done=counts.get("DONE", 0),
            in_progress=counts.get("IN_PROGRESS", 0),
            not_applicable=counts.get("NOT_APPLICABLE", 0),
        ))
    return result


@router.get("/checklist", response_model=list[ChecklistItemOut])
def list_checklist(
    db: Db,
    current_user: Auth,
    area_slug: str | None = Query(None),
    status: str | None = Query(None),
):
    version = _active_version(db)

    q = (
        db.query(ChecklistItem, Mapping, Measure, Area)
        .join(Mapping, Mapping.id == ChecklistItem.mapping_id)
        .join(Measure, Measure.id == Mapping.measure_id)
        .join(Area, Area.id == Mapping.area_id)
        .filter(ChecklistItem.is_active == True)
        .filter(Mapping.is_approved == True)
    )
    if area_slug:
        q = q.filter(Area.slug == area_slug)
    if version:
        q = q.filter(ChecklistItem.bsi_version_id == version.id)

    rows = q.order_by(Area.sort_order, Measure.control_id).all()

    # Batch-load progress and comment counts for this company
    item_ids = [r[0].id for r in rows]
    progress_map: dict[str, Progress] = {}
    comment_counts: dict[str, int] = {}

    if item_ids:
        for p in db.query(Progress).filter(
            Progress.checklist_item_id.in_(item_ids),
            Progress.company_id == current_user.company_id,
        ).all():
            progress_map[p.checklist_item_id] = p

        for ci_id, cnt in db.query(
            Progress.checklist_item_id,
            func.count(Comment.id),
        ).outerjoin(Comment, Comment.progress_id == Progress.id).filter(
            Progress.checklist_item_id.in_(item_ids),
            Progress.company_id == current_user.company_id,
        ).group_by(Progress.checklist_item_id).all():
            comment_counts[ci_id] = cnt

    result = []
    for item, mapping, measure, area in rows:
        prog = progress_map.get(item.id)
        if status and (prog.status if prog else "OPEN") != status:
            continue
        result.append(ChecklistItemOut(
            id=item.id,
            short_description=mapping.short_description,
            confidence=mapping.confidence,
            priority=item.priority,
            area_slug=area.slug,
            area_name=area.name,
            measure=MeasureRef.model_validate(measure),
            status=prog.status if prog else "OPEN",
            progress_id=prog.id if prog else None,
            updated_at=prog.updated_at if prog else None,
            comment_count=comment_counts.get(item.id, 0),
        ))
    return result


@router.get("/checklist/{item_id}", response_model=ChecklistItemOut)
def get_checklist_item(item_id: str, db: Db, current_user: Auth):
    from fastapi import HTTPException
    row = (
        db.query(ChecklistItem, Mapping, Measure, Area)
        .join(Mapping, Mapping.id == ChecklistItem.mapping_id)
        .join(Measure, Measure.id == Mapping.measure_id)
        .join(Area, Area.id == Mapping.area_id)
        .filter(ChecklistItem.id == item_id)
        .filter(ChecklistItem.is_active == True)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Checklist item not found")

    item, mapping, measure, area = row
    prog = db.query(Progress).filter_by(
        checklist_item_id=item.id,
        company_id=current_user.company_id,
    ).first()
    cnt = (
        db.query(func.count(Comment.id))
        .join(Progress, Progress.id == Comment.progress_id)
        .filter(Progress.checklist_item_id == item.id,
                Progress.company_id == current_user.company_id)
        .scalar() or 0
    )
    return ChecklistItemOut(
        id=item.id,
        short_description=mapping.short_description,
        confidence=mapping.confidence,
        priority=item.priority,
        area_slug=area.slug,
        area_name=area.name,
        measure=MeasureRef.model_validate(measure),
        status=prog.status if prog else "OPEN",
        progress_id=prog.id if prog else None,
        updated_at=prog.updated_at if prog else None,
        comment_count=cnt,
    )
