"""FastAPI 앱 진입점"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import ChartRequest, ChartResponse
from app.services.chart import calculate_chart
from app.utils.geocoding import geocode
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


@app.get("/health")
def health_check():
    """헬스체크"""
    return {"status": "healthy"}


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
    
    # 4. 응답 조합
    return ChartResponse(
        planets=chart_data["planets"],
        houses=chart_data["houses"],
        aspects=chart_data["aspects"],
        ascendant=chart_data["ascendant"],
        input={
            "birth_date": request.birth_date,
            "birth_time": request.birth_time,
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone_str
        }
    )
