from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies import get_db, templates, ChartInputData, CONFIG_signs, signSymbols
from app.db_models import ChartRecord

router = APIRouter(tags=["Pages"])

@router.get("/")
async def read_root(request: Request):
    """랜딩 페이지"""
    seo_data = {
        "title": "Cosmic Natal Chart | Free Astrology Analysis",
        "description": "Discover your destiny with our free natal chart calculator."
    }
    return templates.TemplateResponse("index.html", {
        "request": request,
        "seo_data": seo_data
    })

@router.get("/dashboard")
async def dashboard(
    request: Request,
    name: Optional[str] = None,
    birth_date: Optional[str] = None,
    birth_time: Optional[str] = None,
    place_name: Optional[str] = None,
    gender: Optional[str] = "unknown",
    db: Session = Depends(get_db)
):
    """메인 대시보드 (SSR + HTMX)"""
    
    # 1. Load History
    history_list = db.query(ChartRecord).order_by(ChartRecord.created_at.desc()).all()
    
    chart_data = None
    input_data = {
        "name": name or "",
        "birth_date": birth_date or "",
        "birth_time": birth_time or "",
        "place_name": place_name or "",
        "gender": gender
    }
    
    # 2. SSR Calculation (If params provided)
    if birth_date and birth_time and place_name:
        try:
            ci = ChartInputData(name or "Unknown", birth_date, birth_time, place_name, gender)
            await ci.resolve_location()
            chart_data = ci.calculate()
            chart_data['summary_prompt'] = ""
        except Exception as e:
            print(f"SSR Error: {e}")
            
    seo_data = {
        "title": f"Natal Chart - {name}" if name else "My Natal Chart",
        "description": "Detailed astrology analysis dashboard."
    }

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "chart_data": chart_data,
        "input_data": input_data,
        "history_list": history_list,
        "seo_data": seo_data,
        "CONFIG_signs": CONFIG_signs,
        "signSymbols": signSymbols
    })
