"""차트 계산 메인 로직 - 모든 서비스 오케스트레이션"""
from .planets import calculate_planets, calculate_ascendant, format_degree
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
        차트 데이터 (planets, houses, aspects, ascendant)
    """
    # 1. ASC 계산
    asc_longitude, asc_sign, asc_sign_ko, asc_degree = calculate_ascendant(
        birth_date, birth_time, latitude, longitude, timezone_str
    )
    
    # 2. 천체 위치 계산
    planets = calculate_planets(birth_date, birth_time, timezone_str)
    
    # 3. 각 천체의 하우스 배정
    for planet in planets:
        planet["house"] = get_planet_house(planet["position"], asc_longitude)
    
    # 4. 하우스 계산 (Whole Sign)
    houses = calculate_houses(asc_longitude)
    
    # 5. 애스펙트 계산
    aspects = calculate_aspects(planets)
    
    return {
        "planets": planets,
        "houses": houses,
        "aspects": aspects,
        "ascendant": {
            "sign": asc_sign,
            "sign_ko": asc_sign_ko,
            "degree": round(asc_degree, 2),
            "degree_formatted": format_degree(asc_degree)
        }
    }

