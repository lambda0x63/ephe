"""
Dependencies - FastAPI 의존성 주입
"""
from fastapi.templating import Jinja2Templates
from app.database import SessionLocal
from app.constants import ZODIAC_SIGNS, ZODIAC_SYMBOLS

# 템플릿 설정
templates = Jinja2Templates(directory="app/templates")
templates.env.add_extension("jinja2.ext.do")

# 템플릿에서 사용할 상수 (하위호환)
CONFIG_signs = ZODIAC_SIGNS
signSymbols = ZODIAC_SYMBOLS


def get_db():
    """데이터베이스 세션 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
