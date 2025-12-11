"""천체 위치 계산 (Swiss Ephemeris)"""
import swisseph as swe
from datetime import datetime
import pytz


# 7개 전통 천체 (고전점성술)
# (영문, 심볼, 한국어)
PLANETS = {
    swe.SUN: ("Sun", "☉", "태양"),
    swe.MOON: ("Moon", "☽", "달"),
    swe.MERCURY: ("Mercury", "☿", "수성"),
    swe.VENUS: ("Venus", "♀", "금성"),
    swe.MARS: ("Mars", "♂", "화성"),
    swe.JUPITER: ("Jupiter", "♃", "목성"),
    swe.SATURN: ("Saturn", "♄", "토성"),
}

# 12 사인
# (영문, 심볼, 한국어)
SIGNS = [
    ("Aries", "♈", "양자리"), ("Taurus", "♉", "황소자리"),
    ("Gemini", "♊", "쌍둥이자리"), ("Cancer", "♋", "게자리"),
    ("Leo", "♌", "사자자리"), ("Virgo", "♍", "처녀자리"),
    ("Libra", "♎", "천칭자리"), ("Scorpio", "♏", "전갈자리"),
    ("Sagittarius", "♐", "사수자리"), ("Capricorn", "♑", "염소자리"),
    ("Aquarius", "♒", "물병자리"), ("Pisces", "♓", "물고기자리")
]


def get_sign(longitude: float) -> tuple[str, str, str, float]:
    """
    황도 경도(0-360)를 사인과 사인 내 도수로 변환
    
    Returns:
        (sign_name, sign_symbol, sign_name_ko, degree_in_sign)
    """
    sign_index = int(longitude / 30)
    degree_in_sign = longitude % 30
    sign_en, sign_symbol, sign_ko = SIGNS[sign_index]
    return (sign_en, sign_symbol, sign_ko, degree_in_sign)


def format_degree(decimal_degree: float) -> str:
    """
    소수점 도수를 도°분' 형식으로 변환
    
    Args:
        decimal_degree: 18.92
        
    Returns:
        "18°55'"
    """
    degrees = int(decimal_degree)
    minutes = int((decimal_degree - degrees) * 60)
    return f"{degrees}°{minutes:02d}'"


def datetime_to_julian_day(dt: datetime, timezone_str: str) -> float:
    """datetime을 Julian Day로 변환"""
    tz = pytz.timezone(timezone_str)
    local_dt = tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.UTC)
    
    jd = swe.julday(
        utc_dt.year,
        utc_dt.month,
        utc_dt.day,
        utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    )
    return jd


def calculate_planets(birth_date: str, birth_time: str, timezone_str: str) -> list[dict]:
    """
    7개 전통 천체의 위치 계산
    
    Args:
        birth_date: "1990-01-15"
        birth_time: "14:30:00"
        timezone_str: "Asia/Seoul"
        
    Returns:
        천체 정보 리스트
    """
    # datetime 파싱
    dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
    jd = datetime_to_julian_day(dt, timezone_str)
    
    planets = []
    
    for planet_id, (name, symbol, name_ko) in PLANETS.items():
        # 천체 위치 계산 (황도 경도, 위도, 거리, 속도 등)
        result, flag = swe.calc_ut(jd, planet_id)
        longitude = result[0]  # 황도 경도 (0-360)
        speed = result[3]      # 일간 이동 속도
        
        sign_en, sign_symbol, sign_ko, degree = get_sign(longitude)
        retrograde = speed < 0
        
        planets.append({
            "name": name,
            "name_ko": name_ko,
            "symbol": symbol,
            "sign": sign_en,
            "sign_ko": sign_ko,
            "degree": round(degree, 2),
            "degree_formatted": format_degree(degree),
            "retrograde": retrograde,
            "position": round(longitude, 2),
            "house": 0 
        })
    
    return planets


def calculate_ascendant(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone_str: str) -> tuple[float, str, str, float]:
    """
    ASC(Ascendant) 계산
    
    Returns:
        (asc_longitude, sign_en, sign_ko, degree_in_sign)
    """
    dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
    jd = datetime_to_julian_day(dt, timezone_str)
    
    # 하우스 계산 (Whole Sign이라도 ASC는 필요)
    # 'W' = Whole Sign
    houses, ascmc = swe.houses(jd, latitude, longitude, b'W')
    
    asc_longitude = ascmc[0]
    sign_en, sign_symbol, sign_ko, degree = get_sign(asc_longitude)
    
    return (asc_longitude, sign_en, sign_ko, degree)

