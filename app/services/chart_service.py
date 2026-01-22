"""
Chart Service - 차트 생성 통합 서비스
순수 네이탈 차트 전용
"""
from dataclasses import dataclass, field
from typing import Optional
from app.services.chart import calculate_natal_chart
from app.utils.geocoding import get_coordinates
from app.utils.timezone import get_timezone


class ChartError(Exception):
    """차트 계산 관련 에러"""
    def __init__(self, message: str, code: str = "CHART_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


@dataclass
class ChartInput:
    """차트 입력 데이터"""
    name: str
    birth_date: str
    birth_time: str
    place_name: str
    lat: Optional[float] = field(default=None, init=False)
    lon: Optional[float] = field(default=None, init=False)
    tz: Optional[str] = field(default=None, init=False)
    
    def __post_init__(self):
        """입력값 정규화"""
        self._normalize_date()
        self._normalize_time()
    
    def _normalize_date(self):
        """YYYYMMDD -> YYYY-MM-DD"""
        if len(self.birth_date) == 8 and self.birth_date.isdigit():
            self.birth_date = f"{self.birth_date[:4]}-{self.birth_date[4:6]}-{self.birth_date[6:]}"
    
    def _normalize_time(self):
        """HHMM -> HH:MM, HHMMSS -> HH:MM:SS"""
        if self.birth_time.isdigit():
            if len(self.birth_time) == 4:
                self.birth_time = f"{self.birth_time[:2]}:{self.birth_time[2:]}"
            elif len(self.birth_time) == 6:
                self.birth_time = f"{self.birth_time[:2]}:{self.birth_time[2:4]}:{self.birth_time[4:]}"


async def create_chart(
    name: str,
    birth_date: str,
    birth_time: str,
    place_name: str
) -> tuple[dict, ChartInput]:
    """
    네이탈 차트 생성 통합 함수
    
    Returns:
        tuple: (chart_data, chart_input)
        
    Raises:
        ChartError: 위치 조회 실패 또는 계산 오류 시
    """
    # 1. 입력값 정규화
    ci = ChartInput(name, birth_date, birth_time, place_name)
    
    # 2. 위치 정보 조회
    lat, lon = get_coordinates(place_name)
    if lat is None or lon is None:
        raise ChartError(
            f"'{place_name}' 위치를 찾을 수 없습니다.",
            code="LOCATION_NOT_FOUND"
        )
    ci.lat, ci.lon = lat, lon
    
    # 3. 타임존 계산
    try:
        ci.tz = get_timezone(lat, lon)
    except Exception as e:
        raise ChartError(f"타임존 계산 실패: {e}", code="TIMEZONE_ERROR")
    
    # 4. 차트 계산
    try:
        chart_data = await calculate_natal_chart(ci.name, ci.birth_date, ci.birth_time, ci.lat, ci.lon, ci.tz)
    except Exception as e:
        raise ChartError(f"차트 계산 오류: {e}", code="CALCULATION_ERROR")
    
    # 5. 메타데이터 추가
    chart_data.update({
        'name': ci.name,
        'birth_date': ci.birth_date,
        'birth_time': ci.birth_time,
        'place_name': ci.place_name,
        'latitude': ci.lat,
        'longitude': ci.lon,
        'timezone': ci.tz
    })
    
    return chart_data, ci
