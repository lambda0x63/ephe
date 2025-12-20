from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import engine
from app import db_models
from app.routers import pages, htmx, api

# DB 테이블 생성 (운영 환경에서는 Alembic 사용 권장)
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Natal Chart Service",
    description="Advanced Astrology Calculation Service with HTMX Dashboard",
    version="2.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory="public"), name="static")

# 라우터 등록
app.include_router(pages.router)
app.include_router(htmx.router)
app.include_router(api.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
