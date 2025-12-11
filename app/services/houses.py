"""하우스 계산 (Whole Sign)"""
from .planets import SIGNS


def calculate_houses(asc_longitude: float) -> list[dict]:
    """
    Whole Sign 하우스 계산
    
    Whole Sign 방식:
    - ASC가 위치한 사인 전체 = 1하우스
    - 각 하우스 = 정확히 1개 사인(30°)
    
    Args:
        asc_longitude: ASC의 황도 경도 (0-360)
        
    Returns:
        12개 하우스 정보 리스트
    """
    # ASC가 위치한 사인 인덱스
    first_house_sign_index = int(asc_longitude / 30)
    
    houses = []
    
    for i in range(12):
        sign_index = (first_house_sign_index + i) % 12
        sign_en, sign_symbol, sign_ko = SIGNS[sign_index]
        
        houses.append({
            "number": i + 1,
            "sign": sign_en,
            "sign_ko": sign_ko,
            "degree": 0.0  # Whole Sign에서는 각 하우스가 사인 0°에서 시작
        })
    
    return houses


def get_planet_house(planet_longitude: float, asc_longitude: float) -> int:
    """
    천체가 어느 하우스에 있는지 계산 (Whole Sign)
    
    Args:
        planet_longitude: 천체의 황도 경도 (0-360)
        asc_longitude: ASC의 황도 경도 (0-360)
        
    Returns:
        하우스 번호 (1-12)
    """
    # ASC가 위치한 사인 인덱스 = 1하우스
    first_house_sign_index = int(asc_longitude / 30)
    
    # 천체가 위치한 사인 인덱스
    planet_sign_index = int(planet_longitude / 30)
    
    # 1하우스 기준으로 몇 번째 사인인지
    house = (planet_sign_index - first_house_sign_index) % 12 + 1
    
    return house
