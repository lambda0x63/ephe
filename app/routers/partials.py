from fastapi import APIRouter, Request, Form, Depends
from sqlalchemy.orm import Session
import json

from app.dependencies import get_db, templates
from app.services.chart_service import create_chart, ChartError
from app.models import ChartRecord

router = APIRouter(prefix="/partials", tags=["Partials"])


@router.post("/analyze")
async def htmx_analyze(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(...),
    birth_time: str = Form(...),
    place_name: str = Form(...),
    db: Session = Depends(get_db)
):
    """차트 분석 (HTMX partial 반환 + 자동 저장)"""
    try:
        chart_data, chart_input = await create_chart(name, birth_date, birth_time, place_name)
        
        # 중복 체크 (이름, 날짜, 시간, 장소 기반)
        existing = db.query(ChartRecord).filter(
            ChartRecord.name == name,
            ChartRecord.birth_date == chart_input.birth_date,
            ChartRecord.birth_time == chart_input.birth_time,
            ChartRecord.place_name == place_name
        ).first()

        saved = False
        if not existing:
            record = ChartRecord(
                name=name,
                birth_date=chart_input.birth_date,
                birth_time=chart_input.birth_time,
                place_name=place_name,
                latitude=chart_input.lat,
                longitude=chart_input.lon,
                timezone=chart_input.tz,
                gender="",
                chart_data=json.dumps(chart_data)
            )
            db.add(record)
            db.commit()
            saved = True

        response = templates.TemplateResponse("partials/chart_result.html", {
            "request": request,
            "chart_data": chart_data
        })
        
        # 새로운 기록이 저장된 경우에만 목록 새로고침 트리거 발송
        if saved:
            response.headers["HX-Trigger"] = "historyUpdated"
            
        return response
    except ChartError as e:
        return templates.TemplateResponse("partials/error.html", {
            "request": request,
            "error_message": e.message,
            "error_code": e.code
        })
    except Exception as e:
        return templates.TemplateResponse("partials/error.html", {
            "request": request,
            "error_message": f"오류가 발생했습니다: {str(e)}",
            "error_code": "ANALYZE_ERROR"
        })


@router.post("/save")
async def htmx_save(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(...),
    birth_time: str = Form(...),
    place_name: str = Form(...),
    db: Session = Depends(get_db)
):
    """차트 저장 (HTMX partial 반환)"""
    try:
        chart_data, chart_input = await create_chart(name, birth_date, birth_time, place_name)
        
        # Save to DB
        record = ChartRecord(
            name=name,
            birth_date=chart_input.birth_date,
            birth_time=chart_input.birth_time,
            place_name=place_name,
            latitude=chart_input.lat,
            longitude=chart_input.lon,
            timezone=chart_input.tz,
            gender="",
            chart_data=json.dumps(chart_data)
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
        # Return updated list
        history_list = db.query(ChartRecord).order_by(ChartRecord.created_at.desc()).all()
        return templates.TemplateResponse("partials/history_list.html", {
            "request": request,
            "history_list": history_list
        })
    except ChartError as e:
        return templates.TemplateResponse("partials/error.html", {
            "request": request,
            "error_message": e.message,
            "error_code": e.code
        })
    except Exception as e:
        return templates.TemplateResponse("partials/error.html", {
            "request": request,
            "error_message": f"저장 중 오류가 발생했습니다: {str(e)}",
            "error_code": "SAVE_ERROR"
        })


@router.delete("/delete/{chart_id}")
async def htmx_delete(
    request: Request,
    chart_id: int,
    db: Session = Depends(get_db)
):
    """차트 삭제 (HTMX partial 반환)"""
    record = db.query(ChartRecord).filter(ChartRecord.id == chart_id).first()
    if record:
        db.delete(record)
        db.commit()
        
    history_list = db.query(ChartRecord).order_by(ChartRecord.created_at.desc()).all()
    return templates.TemplateResponse("partials/history_list.html", {
        "request": request,
        "history_list": history_list
    })


@router.get("/load/{chart_id}")
async def htmx_load(
    request: Request,
    chart_id: int,
    db: Session = Depends(get_db)
):
    """저장된 차트 로드 (HTMX partial 반환)"""
    record = db.query(ChartRecord).filter(ChartRecord.id == chart_id).first()
    if not record:
        return templates.TemplateResponse("partials/error.html", {
            "request": request,
            "error_message": "해당 기록을 찾을 수 없습니다.",
            "error_code": "NOT_FOUND"
        })
        
    chart_data = json.loads(record.chart_data)
    
    return templates.TemplateResponse("partials/chart_result.html", {
        "request": request,
        "chart_data": chart_data
    })


@router.get("/history")
async def htmx_history(request: Request, db: Session = Depends(get_db)):
    """차트 기록 목록 (HTMX partial 반환)"""
    history_list = db.query(ChartRecord).order_by(ChartRecord.created_at.desc()).all()
    return templates.TemplateResponse("partials/history_list.html", {
        "request": request,
        "history_list": history_list
    })
