"""SQLAlchemy 데이터베이스 모델"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database import Base


class ChartRecord(Base):
    """저장된 네이탈 차트 레코드"""
    __tablename__ = "chart_records"

    id = Column(Integer, primary_key=True, index=True)
    
    # 기본 정보
    name = Column(String, index=True, default="Unknown")
    gender = Column(String, default="unknown")
    birth_date = Column(String(10), nullable=False)  # YYYY-MM-DD
    birth_time = Column(String(8), nullable=False)   # HH:MM:SS
    place_name = Column(String(200), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timezone = Column(String(50), nullable=False)
    
    # 계산된 차트 데이터 (JSON)
    chart_data = Column(JSON, nullable=False)
    
    # AI 프롬프트
    summary_prompt = Column(Text, nullable=True)
    
    # 메타데이터
    created_at = Column(DateTime(timezone=True), server_default=func.now())
