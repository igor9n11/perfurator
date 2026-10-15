from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код до yield выполняется один раз при старте приложения
    create_tables()
    yield


app = FastAPI(title="Perfume Rater", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {})
