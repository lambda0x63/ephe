"""FastAPI 앱 진입점"""
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.models import ChartRequest, ChartResponse
from app.services.chart import calculate_chart
from app.services.summary import generate_ai_summary
from app.utils.geocoding import geocode, search_places
from app.utils.timezone import get_timezone


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
    """네이탈차트 계산"""
    
    # 1. 좌표 확보 (place_name 또는 lat/lng)
    if request.place_name:
        try:
            latitude, longitude = geocode(request.place_name)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif request.latitude is not None and request.longitude is not None:
        latitude = request.latitude
        longitude = request.longitude
    else:
        raise HTTPException(
            status_code=400,
            detail="Either place_name or latitude/longitude is required"
        )
    
    # 2. 타임존 추론
    try:
        timezone_str = get_timezone(latitude, longitude)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # 3. 차트 계산
    chart_data = calculate_chart(
        birth_date=request.birth_date,
        birth_time=request.birth_time,
        latitude=latitude,
        longitude=longitude,
        timezone_str=timezone_str
    )
    
    # 4. AI 요약 리포트 생성
    summary_text = generate_ai_summary(chart_data)
    
    # 5. 응답 조합
    return ChartResponse(
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
        summary_prompt=summary_text
    )
