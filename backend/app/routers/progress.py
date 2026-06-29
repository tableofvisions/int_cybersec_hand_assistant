from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.deps import get_verified_user
from app.database import get_db
from app.models.bsi import ChecklistItem
from app.models.progress import Comment, Progress
from app.models.user import User
from app.schemas.progress import CommentCreate, CommentOut, ProgressOut, ProgressUpdate

router = APIRouter(prefix="/api/v1/progress", tags=["progress"])

Db   = Annotated[Session, Depends(get_db)]
Auth = Annotated[User, Depends(get_verified_user)]


def _get_or_create_progress(
    db: Session, item_id: str, company_id: str
) -> tuple[Progress, bool]:
    prog = db.query(Progress).filter_by(
        checklist_item_id=item_id, company_id=company_id
    ).first()
    if prog:
        return prog, False
    prog = Progress(checklist_item_id=item_id, company_id=company_id, status="OPEN")
    db.add(prog)
    db.flush()
    return prog, True


@router.put("/{item_id}", response_model=ProgressOut)
def update_progress(item_id: str, body: ProgressUpdate, db: Db, current_user: Auth):
    item = db.query(ChecklistItem).filter_by(id=item_id, is_active=True).first()
    if not item:
        raise HTTPException(status_code=404, detail="Checklist item not found")

    prog, _ = _get_or_create_progress(db, item_id, current_user.company_id)
    prog.status = body.status

    if body.status == "DONE":
        prog.completed_at = datetime.now(timezone.utc)
        prog.completed_by = current_user.id
    elif prog.status != "DONE":
        prog.completed_at = None
        prog.completed_by = None

    db.commit()
    db.refresh(prog)
    return prog


@router.get("/{item_id}/comments", response_model=list[CommentOut])
def list_comments(item_id: str, db: Db, current_user: Auth):
    prog = db.query(Progress).filter_by(
        checklist_item_id=item_id, company_id=current_user.company_id
    ).first()
    if not prog:
        return []
    return (
        db.query(Comment)
        .filter_by(progress_id=prog.id)
        .order_by(Comment.created_at)
        .all()
    )


@router.post("/{item_id}/comments", response_model=CommentOut, status_code=201)
def add_comment(item_id: str, body: CommentCreate, db: Db, current_user: Auth):
    item = db.query(ChecklistItem).filter_by(id=item_id, is_active=True).first()
    if not item:
        raise HTTPException(status_code=404, detail="Checklist item not found")

    prog, _ = _get_or_create_progress(db, item_id, current_user.company_id)
    comment = Comment(progress_id=prog.id, user_id=current_user.id, text=body.text)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{item_id}/comments/{comment_id}", status_code=204)
def delete_comment(item_id: str, comment_id: str, db: Db, current_user: Auth):
    comment = (
        db.query(Comment)
        .join(Progress, Progress.id == Comment.progress_id)
        .filter(
            Comment.id == comment_id,
            Progress.checklist_item_id == item_id,
            Progress.company_id == current_user.company_id,
            Comment.user_id == current_user.id,
        )
        .first()
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
