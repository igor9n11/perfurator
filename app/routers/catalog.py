from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.catalog import get_catalog_page
from app.templating import templates

router = APIRouter()


@router.get("/catalog")
def catalog(request: Request, page: int = Query(1, ge=1), db: Session = Depends(get_db)):
    data = get_catalog_page(db, page)
    return templates.TemplateResponse(request, "catalog.html", data)
