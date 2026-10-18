from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app import models  # noqa: F401 — без импорта create_all не увидит таблицы
from app.db import create_tables
from app.routers import catalog
from app.templating import templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Perfume Rater", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(catalog.router)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {})
