from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from app.config import MONGO_DB_NAME, MONGO_URL
from app.models import mongodb

# 절대 경로 지정 (app) 디렉토리 파일 명시
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

templates = Jinja2Templates(directory=BASE_DIR / "templates")

# root 라우터


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("./index.html",
                                      {"request": request, "title": "콜렉터 북북이"})


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    print(q)
    return templates.TemplateResponse("./index.html",
                                      {"request": request, "title": "콜렉터스 북북이", "keyword": q})


@app.on_event("startup")
async def on_app_start():
    """before app starts"""
    # await mongodb.connect()
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    """after app shutdown"""
    print("Bye server")
    # await mongodb.close()
    mongodb.close()
