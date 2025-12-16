"""Pydantic models for Request/Response"""
from pydantic import BaseModel, field_validator
from typing import Optional


class ChartRequest(BaseModel):
    """네이탈차트 계산 요청"""
    name: str  # 차트 소유자 이름
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM:SS
    gender: str = 'unknown'  # male, female, other
    
    # 둘 중 하나 필수
    place_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    @field_validator('birth_date')
    @classmethod
    def validate_date(cls, v):
        from datetime import datetime
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('birth_date must be YYYY-MM-DD format')
        return v
    
    @field_validator('birth_time')
    @classmethod
    def validate_time(cls, v):
        from datetime import datetime
        try:
            datetime.strptime(v, '%H:%M:%S')
        except ValueError:
            raise ValueError('birth_time must be HH:MM:SS format')
        return v


class Planet(BaseModel):
    """천체 정보"""
    name: str
    name_ko: str
    symbol: str
    sign: str
    sign_ko: str
    degree: float  # 사인 내 도수 (0-30)
    degree_formatted: str  # "18°55'"
    house: int
    retrograde: bool
    position: float  # 황도 절대 위치 (0-360)


class House(BaseModel):
    """하우스 정보"""
    number: int
    sign: str
    sign_ko: str
    degree: float


class Aspect(BaseModel):
    """애스펙트 정보"""
    planet1: str
    planet1_ko: str
    planet2: str
    planet2_ko: str
    type: str
    type_ko: str
    angle: int
    orb: float


class Ascendant(BaseModel):
    """ASC 정보"""
    sign: str
    sign_ko: str
    degree: float
    degree_formatted: str  # "16°37'"


class Midheaven(BaseModel):
    """MC(천정) 정보"""
    sign: str
    sign_ko: str
    degree: float
    degree_formatted: str  # "18°31'"


class Fortuna(BaseModel):
    """포르투나(Part of Fortune) 정보"""
    sign: str
    sign_ko: str
    degree: float
    degree_formatted: str
    house: int


class InputInfo(BaseModel):
    """입력 정보 확인용"""
    place_name: Optional[str] = None
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str


class ChartResponse(BaseModel):
    """네이탈차트 응답"""
    id: Optional[int] = None  # DB 저장 시 생성되는 ID
    name: str  # 차트 소유자 이름
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    birth_time: Optional[str] = None
    planets: list[Planet]
    houses: list[House]
    aspects: list[Aspect]
    ascendant: Ascendant
    midheaven: Midheaven
    fortuna: Fortuna
    input: InputInfo
    summary_prompt: Optional[str] = None


class ChartListItem(BaseModel):
    """저장된 차트 목록 아이템"""
    id: int
    name: str
    birth_date: str
    birth_time: str
    place_name: Optional[str]
    created_at: str
