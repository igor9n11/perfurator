import math

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Fragrance

PAGE_SIZE = 30


def get_catalog_page(db: Session, page: int) -> dict:
    total = db.scalar(select(func.count()).select_from(Fragrance))
    pages = max(1, math.ceil(total / PAGE_SIZE))
    page = min(page, pages)

    items = db.scalars(
        select(Fragrance)
        .order_by(Fragrance.source_votes.desc(), Fragrance.id)
        .offset((page - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE)
    ).all()

    return {"items": items, "page": page, "pages": pages, "total": total}
