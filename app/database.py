"""PostgreSQL 데이터베이스 설정"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 환경변수 또는 기본값 사용
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://natal_user:natal_secret_2024@localhost:5432/natal_chart"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI 의존성 주입용 DB 세션"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
