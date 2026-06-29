import math
import random
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, func
from sqlalchemy.orm import Session, joinedload

from app.auth.deps import get_verified_user
from app.database import get_db
from app.models.glossary import GlossaryCategory, GlossaryReference, GlossaryTerm
from app.models.user import User
from app.schemas.glossary import (
    GlossaryCategoryOut,
    GlossaryCategorySearchRequest,
    GlossaryEntryLightOut,
    GlossaryEntryOut,
    GlossarySearchRequest,
    GlossarySearchResult,
    GlossarySourceOut,
    GlossaryTermOut,
)

router = APIRouter(prefix="/api/v1/glossary", tags=["glossary"])

Db = Annotated[Session, Depends(get_db)]
Auth = Annotated[User, Depends(get_verified_user)]


def _term_to_light(term: GlossaryTerm) -> GlossaryEntryLightOut:
    return GlossaryEntryLightOut(
        id=term.id,
        keyword=term.keyword,
        definition=term.definition,
    )


def _build_entry(term: GlossaryTerm) -> GlossaryEntryOut:
    cat = term.category
    cat_out = GlossaryCategoryOut(
        id=cat.id,
        name=cat.name,
        description=cat.description,
        imageSrc=cat.image_src,
    )
    term_out = GlossaryTermOut(
        id=term.id,
        keyword=term.keyword,
        definition=term.definition,
        description=term.description,
        category=cat_out,
        synonyms=[s.value for s in term.synonyms],
        sources=[GlossarySourceOut(id=s.id, name=s.name, url=s.url) for s in term.sources],
        createdAt=term.created_at.isoformat(),
        updatedAt=term.updated_at.isoformat(),
    )
    refs = {ref.referenced_term.keyword: _term_to_light(ref.referenced_term) for ref in term.references}
    return GlossaryEntryOut(term=term_out, category=cat_out, references=refs)


def _load_term(db: Session, term_id: str) -> GlossaryTerm:
    term = (
        db.query(GlossaryTerm)
        .options(
            joinedload(GlossaryTerm.category),
            joinedload(GlossaryTerm.synonyms),
            joinedload(GlossaryTerm.sources),
            joinedload(GlossaryTerm.references).joinedload(GlossaryReference.referenced_term),
        )
        .filter(GlossaryTerm.id == term_id)
        .first()
    )
    if not term:
        raise HTTPException(status_code=404, detail="Glossary entry not found")
    return term


def _paginate(db: Session, q, page: int, size: int) -> GlossarySearchResult:
    total = q.count()
    items = q.offset(page * size).limit(size).all()
    total_pages = math.ceil(total / size) if size else 1
    content = [_term_to_light(t) for t in items]
    return GlossarySearchResult(
        totalPages=total_pages,
        totalElements=total,
        pageable={"pageNumber": page, "pageSize": size},
        numberOfElements=len(content),
        size=size,
        content=content,
        number=page,
        first=(page == 0),
        last=(page >= total_pages - 1),
        empty=(len(content) == 0),
    )


@router.get("/categories", response_model=list[GlossaryCategoryOut])
def list_categories(db: Db, current_user: Auth):
    cats = db.query(GlossaryCategory).order_by(GlossaryCategory.name).all()
    return [
        GlossaryCategoryOut(id=c.id, name=c.name, description=c.description, imageSrc=c.image_src)
        for c in cats
    ]


@router.get("/random", response_model=GlossaryEntryOut)
def random_entry(categoryId: str, db: Db, current_user: Auth):
    cat = db.query(GlossaryCategory).filter(GlossaryCategory.id == categoryId).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    ids = [t.id for t in db.query(GlossaryTerm.id).filter(GlossaryTerm.category_id == categoryId).all()]
    if not ids:
        raise HTTPException(status_code=404, detail="No entries in category")
    chosen_id = random.choice(ids)
    return _build_entry(_load_term(db, chosen_id))


@router.post("/search", response_model=GlossarySearchResult)
def search(body: GlossarySearchRequest, db: Db, current_user: Auth):
    q_str = body.searchCriteria.all.strip()
    page = body.pageable.page
    size = body.pageable.size or 20

    q = db.query(GlossaryTerm).options(joinedload(GlossaryTerm.category))
    if q_str:
        pattern = f"%{q_str}%"
        q = q.filter(
            or_(
                GlossaryTerm.keyword.ilike(pattern),
                GlossaryTerm.definition.ilike(pattern),
                GlossaryTerm.description.ilike(pattern),
            )
        )
    q = q.order_by(GlossaryTerm.keyword)
    return _paginate(db, q, page, size)


@router.post("/search-by-category", response_model=GlossarySearchResult)
def search_by_category(body: GlossaryCategorySearchRequest, db: Db, current_user: Auth):
    page = body.pageable.page
    size = body.pageable.size or 9999

    q = (
        db.query(GlossaryTerm)
        .join(GlossaryCategory)
        .filter(GlossaryCategory.name.ilike(f"%{body.category.strip()}%"))
        .order_by(GlossaryTerm.keyword)
    )
    return _paginate(db, q, page, size)


@router.get("/{term_id}", response_model=GlossaryEntryOut)
def get_entry(term_id: str, db: Db, current_user: Auth):
    return _build_entry(_load_term(db, term_id))
