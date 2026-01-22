from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies import get_db, templates, CONFIG_signs, signSymbols
from app.services.chart_service import create_chart, ChartError
from app.models import ChartRecord

router = APIRouter(tags=["Pages"])


@router.get("/")
async def read_root(request: Request):
    """랜딩 페이지"""
    seo_data = {
        "title": "Ephe - Natal Archive",
        "description": "Discover your destiny with Ephe - your classical astrology companion."
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
    error_message = None
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
            chart_data, _ = await create_chart(
                name or "Unknown",
                birth_date,
                birth_time,
                place_name,
                gender
            )
            chart_data['summary_prompt'] = ""
        except ChartError as e:
            error_message = e.message
        except Exception as e:
            error_message = f"차트 계산 중 오류: {str(e)}"
            
    seo_data = {
        "title": f"Ephe - {name}" if name else "Ephe - Natal Archive",
        "description": "Detailed astrology analysis dashboard."
    }

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "chart_data": chart_data,
        "input_data": input_data,
        "history_list": history_list,
        "error_message": error_message,
        "seo_data": seo_data,
        "CONFIG_signs": CONFIG_signs,
        "signSymbols": signSymbols
    })
