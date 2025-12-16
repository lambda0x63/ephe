"""FastAPI 앱 진입점"""
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.models import ChartRequest, ChartResponse, ChartListItem
from app.services.chart import calculate_chart
from app.services.summary import generate_ai_summary
from app.utils.geocoding import geocode, search_places
from app.utils.timezone import get_timezone
from app.database import engine, get_db, Base
from app.db_models import ChartRecord


# 테이블 자동 생성
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Natal Chart API",
    description="고전점성술 기반 네이탈차트 계산 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 서빙 (public 폴더)
PUBLIC_DIR = Path(__file__).parent.parent / "public"
if PUBLIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=PUBLIC_DIR), name="static")


@app.get("/")
def root():
    """루트 경로 - index.html 반환"""
    index_path = PUBLIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Natal Chart API", "docs": "/docs"}


@app.get("/health")
def health_check():
    """헬스체크"""
    return {"status": "healthy"}


@app.get("/api/v1/search-place")
def search_place_api(query: str):
    """도시 검색 (Autocomplete용)"""
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    try:
        results = search_places(query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/natal-chart", response_model=ChartResponse)
def create_natal_chart(request: ChartRequest):
    """네이탈차트 단순 계산 (저장 X)"""
    
    # 1. 좌표 확보
    if request.place_name:
        try:
            latitude, longitude = geocode(request.place_name)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif request.latitude is not None and request.longitude is not None:
        latitude = request.latitude
        longitude = request.longitude
    else:
        raise HTTPException(status_code=400, detail="Location required")
    
    # 2. 타임존
    try:
        timezone_str = get_timezone(latitude, longitude)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # 3. 계산
    chart_data = calculate_chart(request.birth_date, request.birth_time, latitude, longitude, timezone_str)
    
    # 4. Generate AI Summary Prompt
    summary = generate_ai_summary(chart_data, request.name, request.gender, request.birth_date, request.birth_time, request.place_name)
    
    return ChartResponse(
        name=request.name,
        gender=request.gender,
        birth_date=request.birth_date,
        birth_time=request.birth_time,
        planets=chart_data["planets"],
        houses=chart_data["houses"],
        aspects=chart_data["aspects"],
        ascendant=chart_data["ascendant"],
        midheaven=chart_data["midheaven"],
        fortuna=chart_data["fortuna"],
        input={
            "birth_date": request.birth_date,
            "birth_time": request.birth_time,
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone_str
        },
        summary_prompt=summary
    )


@app.post("/api/v1/charts", response_model=ChartResponse)
def save_chart(request: ChartRequest, db: Session = Depends(get_db)):
    """차트 계산 후 DB 저장"""
    # (로직 재사용을 위해 내부 호출 가능하지만, 명시적으로 다시 수행)
    
    # 1. 좌표
    if request.place_name:
        try:
            lat, lng = geocode(request.place_name)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif request.latitude and request.longitude:
        lat, lng = request.latitude, request.longitude
    else:
        raise HTTPException(status_code=400, detail="Location required")
        
    # 2. 타임존
    try:
        tz = get_timezone(lat, lng)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # 3. 계산
    chart_data = calculate_chart(request.birth_date, request.birth_time, lat, lng, tz)
    # 4. Generate AI Summary Prompt
    summary = generate_ai_summary(chart_data, request.name, request.gender, request.birth_date, request.birth_time, request.place_name)
    
    # 5. 저장
    db_record = ChartRecord(
        name=request.name,
        gender=request.gender,
        birth_date=request.birth_date,
        birth_time=request.birth_time,
        place_name=request.place_name,
        latitude=lat,
        longitude=lng,
        timezone=tz,
        chart_data=chart_data,
        summary_prompt=summary
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return ChartResponse(
        id=db_record.id,
        name=request.name,
        gender=request.gender,
        planets=chart_data["planets"],
        houses=chart_data["houses"],
        aspects=chart_data["aspects"],
        ascendant=chart_data["ascendant"],
        midheaven=chart_data["midheaven"],
        fortuna=chart_data["fortuna"],
        input={
            "birth_date": request.birth_date,
            "birth_time": request.birth_time,
            "latitude": lat,
            "longitude": lng,
            "timezone": tz
        },
        summary_prompt=summary
    )


@app.get("/api/v1/charts", response_model=list[ChartListItem])
def list_saved_charts(db: Session = Depends(get_db)):
    """저장된 차트 목록 조회"""
    charts = db.query(ChartRecord).order_by(ChartRecord.created_at.desc()).all()
    return [
        ChartListItem(
            id=record.id,
            name=record.name,
            gender=record.gender,
            birth_date=record.birth_date,
            birth_time=record.birth_time,
            place_name=record.place_name,
            created_at=record.created_at.strftime("%Y-%m-%d %H:%M:%S")
        ) for record in charts
    ]


@app.delete("/api/v1/charts/{chart_id}")
def delete_chart(chart_id: int, db: Session = Depends(get_db)):
    """차트 삭제"""
    chart = db.query(ChartRecord).filter(ChartRecord.id == chart_id).first()
    if not chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    
    db.delete(chart)
    db.commit()
    return {"message": "Deleted successfully"}
