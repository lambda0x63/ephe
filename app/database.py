"""데이터베이스 설정 (SQLite 또는 PostgreSQL)"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 환경변수 또는 기본값 사용 (개발: SQLite, 프로덕션: PostgreSQL)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./ephe.db"  # 개발용 SQLite
)

# SQLite 연결 설정
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI 의존성 주입용 DB 세션"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
