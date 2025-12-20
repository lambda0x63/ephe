from fastapi import APIRouter, Request, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.dependencies import get_db, templates, ChartInputData
from app.db_models import ChartRecord

router = APIRouter(prefix="/htmx", tags=["HTMX"])

@router.post("/analyze")
async def htmx_analyze(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(...),
    birth_time: str = Form(...),
    place_name: str = Form(...),
    gender: str = Form("unknown")
):
    # 1. Input Object
    input_data = ChartInputData(name, birth_date, birth_time, place_name, gender)
    await input_data.resolve_location()
    
    # 2. Calculate
    chart_data = input_data.calculate()
    chart_data['summary_prompt'] = ""  # 기능 제거됨
    
    return templates.TemplateResponse("partials/chart_result.html", {
        "request": request,
        "chart_data": chart_data
    })


@router.post("/save")
async def htmx_save(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(...),
    birth_time: str = Form(...),
    place_name: str = Form(...),
    gender: str = Form("unknown"),
    db: Session = Depends(get_db)
):
    input_data = ChartInputData(name, birth_date, birth_time, place_name, gender)
    await input_data.resolve_location()
    chart_data = input_data.calculate()
    chart_data['summary_prompt'] = ""
    
    # Save to DB
    record = ChartRecord(
        name=name,
        birth_date=birth_date,
        birth_time=birth_time,
        place_name=place_name,
        latitude=input_data.lat,
        longitude=input_data.lon,
        timezone=input_data.tz,
        gender=gender,
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


@router.delete("/delete/{chart_id}")
async def htmx_delete(
    request: Request,
    chart_id: int,
    db: Session = Depends(get_db)
):
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
    record = db.query(ChartRecord).filter(ChartRecord.id == chart_id).first()
    if not record:
        return ""
        
    chart_data = json.loads(record.chart_data)
    
    return templates.TemplateResponse("partials/chart_result.html", {
        "request": request,
        "chart_data": chart_data
    })
