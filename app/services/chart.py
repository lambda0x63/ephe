"""차트 계산 메인 로직 - 모든 서비스 오케스트레이션"""
from .planets import (
    calculate_planets, 
    calculate_angles, 
    calculate_fortuna,
    is_day_chart,
    format_degree,
    get_sign
)
from .houses import calculate_houses, get_planet_house
from .aspects import calculate_aspects


def calculate_chart(
    birth_date: str,
    birth_time: str,
    latitude: float,
    longitude: float,
    timezone_str: str
) -> dict:
    """
    네이탈차트 전체 계산
    
    Args:
        birth_date: "1990-01-15"
        birth_time: "14:30:00"
        latitude: 위도
        longitude: 경도
        timezone_str: "Asia/Seoul"
        
    Returns:
        차트 데이터 (planets, houses, aspects, ascendant, midheaven, fortuna)
    """
    # 1. ASC, MC 계산
    angles = calculate_angles(
        birth_date, birth_time, latitude, longitude, timezone_str
    )
    asc_longitude, asc_sign, asc_sign_ko, asc_degree = angles["asc"]
    mc_longitude, mc_sign, mc_sign_ko, mc_degree = angles["mc"]
    
    # 2. 천체 위치 계산
    planets = calculate_planets(birth_date, birth_time, timezone_str)
    
    # 3. 각 천체의 하우스 배정
    for planet in planets:
        planet["house"] = get_planet_house(planet["position"], asc_longitude)
    
    # 4. 하우스 계산 (Whole Sign)
    houses = calculate_houses(asc_longitude)
    
    # 5. 애스펙트 계산
    aspects = calculate_aspects(planets)
    
    # 6. 포르투나 계산
    sun_pos = next(p["position"] for p in planets if p["name"] == "Sun")
    moon_pos = next(p["position"] for p in planets if p["name"] == "Moon")
    
    is_day = is_day_chart(sun_pos, asc_longitude)
    fortuna_longitude = calculate_fortuna(sun_pos, moon_pos, asc_longitude, is_day)
    
    fortuna_sign_en, _, fortuna_sign_ko, fortuna_degree = get_sign(fortuna_longitude)
    fortuna_house = get_planet_house(fortuna_longitude, asc_longitude)
    
    return {
        "planets": planets,
        "houses": houses,
        "aspects": aspects,
        "ascendant": {
            "sign": asc_sign,
            "sign_ko": asc_sign_ko,
            "degree": round(asc_degree, 2),
            "degree_formatted": format_degree(asc_degree)
        },
        "midheaven": {
            "sign": mc_sign,
            "sign_ko": mc_sign_ko,
            "degree": round(mc_degree, 2),
            "degree_formatted": format_degree(mc_degree)
        },
        "fortuna": {
            "sign": fortuna_sign_en,
            "sign_ko": fortuna_sign_ko,
            "degree": round(fortuna_degree, 2),
            "degree_formatted": format_degree(fortuna_degree),
            "house": fortuna_house
        }
    }
