"""천체 위치 계산 (Swiss Ephemeris)"""
import swisseph as swe
from datetime import datetime
import pytz


# 7개 전통 천체 (고전점성술)
# (영문, 심볼, 한국어)
PLANETS = {
    swe.SUN: ("Sun", "☉", "태양", "fire"),
    swe.MOON: ("Moon", "☾", "달", "water"),
    swe.MERCURY: ("Mercury", "☿", "수성", "air"), # Air/Neutral variable nature
    swe.VENUS: ("Venus", "♀", "금성", "water"),
    swe.MARS: ("Mars", "♂", "화성", "fire"),
    swe.JUPITER: ("Jupiter", "♃", "목성", "air"),
    swe.SATURN: ("Saturn", "♄", "토성", "earth"),
}

# 12 사인
# (영문, 심볼, 한국어)
SIGNS = [
    ("Aries", "♈︎", "양자리", "fire"), ("Taurus", "♉︎", "황소자리", "earth"),
    ("Gemini", "♊︎", "쌍둥이자리", "air"), ("Cancer", "♋︎", "게자리", "water"),
    ("Leo", "♌︎", "사자자리", "fire"), ("Virgo", "♍︎", "처녀자리", "earth"),
    ("Libra", "♎︎", "천칭자리", "air"), ("Scorpio", "♏︎", "전갈자리", "water"),
    ("Sagittarius", "♐︎", "사수자리", "fire"), ("Capricorn", "♑︎", "염소자리", "earth"),
    ("Aquarius", "♒︎", "물병자리", "air"), ("Pisces", "♓︎", "물고기자리", "water")
]


# 고전점성술 룰러십 (Sign -> Planet Name)
RULERSHIPS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter"
}


def get_ruler_planet(sign_name: str) -> str:
    """별자리의 주인 행성(Ruler) 반환"""
    return RULERSHIPS.get(sign_name)


# ============================================================
# Essential Dignities (Hellenistic - Ptolemy's Tetrabiblos)
# ============================================================
# 각 행성별 Domicile(본궁), Exaltation(고양), Detriment(손상), Fall(추락)
# Peregrine(이방인)은 위 4가지 중 어느 것도 아닌 경우

ESSENTIAL_DIGNITIES = {
    "Sun": {
        "domicile": ["Leo"],
        "exaltation": ["Aries"],
        "detriment": ["Aquarius"],
        "fall": ["Libra"]
    },
    "Moon": {
        "domicile": ["Cancer"],
        "exaltation": ["Taurus"],
        "detriment": ["Capricorn"],
        "fall": ["Scorpio"]
    },
    "Mercury": {
        "domicile": ["Gemini", "Virgo"],
        "exaltation": ["Virgo"],
        "detriment": ["Sagittarius", "Pisces"],
        "fall": ["Pisces"]
    },
    "Venus": {
        "domicile": ["Taurus", "Libra"],
        "exaltation": ["Pisces"],
        "detriment": ["Scorpio", "Aries"],
        "fall": ["Virgo"]
    },
    "Mars": {
        "domicile": ["Aries", "Scorpio"],
        "exaltation": ["Capricorn"],
        "detriment": ["Libra", "Taurus"],
        "fall": ["Cancer"]
    },
    "Jupiter": {
        "domicile": ["Sagittarius", "Pisces"],
        "exaltation": ["Cancer"],
        "detriment": ["Gemini", "Virgo"],
        "fall": ["Capricorn"]
    },
    "Saturn": {
        "domicile": ["Capricorn", "Aquarius"],
        "exaltation": ["Libra"],
        "detriment": ["Cancer", "Leo"],
        "fall": ["Aries"]
    }
}


def get_planet_dignity(planet_name: str, sign_name: str) -> str:
    """
    행성의 Essential Dignity(품위) 판정
    
    Args:
        planet_name: "Mars", "Venus" 등 영문 행성명
        sign_name: "Aries", "Libra" 등 영문 별자리명
        
    Returns:
        "Domicile" | "Exaltation" | "Detriment" | "Fall" | "Peregrine"
    """
    dignities = ESSENTIAL_DIGNITIES.get(planet_name)
    if not dignities:
        return "Peregrine"
    
    if sign_name in dignities["domicile"]:
        return "Domicile"
    elif sign_name in dignities["exaltation"]:
        return "Exaltation"
    elif sign_name in dignities["detriment"]:
        return "Detriment"
    elif sign_name in dignities["fall"]:
        return "Fall"
    else:
        return "Peregrine"


def get_dignity_description(dignity: str) -> str:
    """품위에 대한 한글 설명"""
    descriptions = {
        "Domicile": "본궁 (Domicile)",
        "Exaltation": "고양 (Exaltation)",
        "Triplicity": "삼궁 (Triplicity)",
        "Term": "경계 (Term/Bound)",
        "Face": "데칸 (Face/Decan)",
        "Detriment": "손상 (Detriment)",
        "Fall": "추락 (Fall)",
        "Peregrine": "이방인 (Peregrine)"
    }
    return descriptions.get(dignity, dignity)

# ============================================================
# Hellenistic 5-Dignity Tables
# ============================================================

# 1. Triplicity Rulers (Dorothean)
# (Day Ruler, Night Ruler, Participating Ruler)
TRIPLICITY_RULERS = {
    "fire": ("Sun", "Jupiter", "Saturn"),
    "earth": ("Venus", "Moon", "Mars"),
    "air": ("Saturn", "Mercury", "Jupiter"),
    "water": ("Venus", "Mars", "Moon")
}

def get_triplicity_ruler(element: str, is_day: bool) -> str:
    rulers = TRIPLICITY_RULERS.get(element)
    if not rulers: return "Unknown"
    return rulers[0] if is_day else rulers[1]

# 2. Egyptian Terms (Bounds)
# Format: Sign -> List of (End Degree, Planet)
EGYPTIAN_TERMS = {
    "Aries": [(6, "Jupiter"), (12, "Venus"), (20, "Mercury"), (25, "Mars"), (30, "Saturn")],
    "Taurus": [(8, "Venus"), (14, "Mercury"), (22, "Jupiter"), (27, "Saturn"), (30, "Mars")],
    "Gemini": [(6, "Mercury"), (12, "Jupiter"), (17, "Venus"), (24, "Mars"), (30, "Saturn")],
    "Cancer": [(7, "Mars"), (13, "Venus"), (19, "Mercury"), (26, "Jupiter"), (30, "Saturn")],
    "Leo": [(6, "Jupiter"), (11, "Venus"), (18, "Saturn"), (24, "Mercury"), (30, "Mars")],
    "Virgo": [(7, "Mercury"), (17, "Venus"), (21, "Jupiter"), (28, "Mars"), (30, "Saturn")],
    "Libra": [(6, "Saturn"), (14, "Venus"), (21, "Jupiter"), (28, "Mercury"), (30, "Mars")],
    "Scorpio": [(7, "Mars"), (11, "Venus"), (19, "Mercury"), (24, "Jupiter"), (30, "Saturn")],
    "Sagittarius": [(12, "Jupiter"), (17, "Venus"), (21, "Mercury"), (26, "Saturn"), (30, "Mars")],
    "Capricorn": [(7, "Mercury"), (14, "Jupiter"), (22, "Venus"), (26, "Saturn"), (30, "Mars")],
    "Aquarius": [(7, "Saturn"), (13, "Mercury"), (20, "Venus"), (25, "Jupiter"), (30, "Mars")],
    "Pisces": [(12, "Venus"), (16, "Jupiter"), (19, "Mercury"), (28, "Mars"), (30, "Saturn")]
}

def get_term_ruler(sign: str, degree: float) -> str:
    terms = EGYPTIAN_TERMS.get(sign)
    if not terms: return "Unknown"
    for end_deg, planet in terms:
        if degree < end_deg:
            return planet
    return terms[-1][1]

# 3. Chaldean Faces (Decans)
# 10 degrees each, following the Chaldean order: Sat, Jup, Mar, Sun, Ven, Mer, Moo
CHALDEAN_FACES = [
    "Mars", "Sun", "Venus",       # Aries
    "Mercury", "Moon", "Saturn",    # Taurus
    "Jupiter", "Mars", "Sun",       # Gemini
    "Venus", "Mercury", "Moon",     # Cancer
    "Saturn", "Jupiter", "Mars",    # Leo
    "Sun", "Venus", "Mercury",      # Virgo
    "Moon", "Saturn", "Jupiter",    # Libra
    "Mars", "Sun", "Venus",         # Scorpio
    "Mercury", "Moon", "Saturn",    # Sagittarius
    "Jupiter", "Mars", "Sun",       # Capricorn
    "Venus", "Mercury", "Moon",     # Aquarius
    "Saturn", "Jupiter", "Mars"     # Pisces
]

def get_face_ruler(longitude: float) -> str:
    face_index = int(longitude / 10) % 36
    return CHALDEAN_FACES[face_index]


def get_sign(longitude: float) -> tuple[str, str, str, str, float]:
    """
    황도 경도(0-360)를 사인과 사인 내 도수로 변환
    
    Returns:
        (sign_name, sign_symbol, sign_name_ko, element, degree_in_sign)
    """
    sign_index = int(longitude / 30)
    degree_in_sign = longitude % 30
    sign_en, sign_symbol, sign_ko, element = SIGNS[sign_index]
    return (sign_en, sign_symbol, sign_ko, element, degree_in_sign)


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


from app.utils.datetime import parse_birth_datetime


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
    dt = parse_birth_datetime(birth_date, birth_time)
    jd = datetime_to_julian_day(dt, timezone_str)
    
    planets = []
    
    for planet_id, (name, symbol, name_ko, p_element) in PLANETS.items():
        # 천체 위치 계산 (황도 경도, 위도, 거리, 속도 등)
        result, flag = swe.calc_ut(jd, planet_id)
        longitude = result[0]  # 황도 경도 (0-360)
        speed = result[3]      # 일간 이동 속도
        
        sign_en, sign_symbol, sign_ko, s_element, degree = get_sign(longitude)
        retrograde = speed < 0
        
        planets.append({
            "name": name,
            "name_ko": name_ko,
            "symbol": symbol,
            "sign": sign_en,
            "sign_ko": sign_ko,
            "sign_element": s_element,
            "planet_element": p_element,
            "degree": round(degree, 2),
            "degree_formatted": format_degree(degree),
            "retrograde": retrograde,
            "position": round(longitude, 2),
            "house": 0 
        })
    
    return planets


def calculate_angles(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone_str: str) -> dict:
    """
    ASC(Ascendant)와 MC(Midheaven) 계산
    
    Returns:
        {
            "asc": (longitude, sign_en, sign_ko, degree_in_sign),
            "mc": (longitude, sign_en, sign_ko, degree_in_sign)
        }
    """
    dt = parse_birth_datetime(birth_date, birth_time)
    jd = datetime_to_julian_day(dt, timezone_str)
    
    # 하우스 계산 (Whole Sign이라도 ASC는 필요)
    # 'W' = Whole Sign
    houses, ascmc = swe.houses(jd, latitude, longitude, b'W')
    
    # ASC = ascmc[0], MC = ascmc[1]
    asc_longitude = ascmc[0]
    mc_longitude = ascmc[1]
    
    asc_sign_en, _, asc_sign_ko, asc_element, asc_degree = get_sign(asc_longitude)
    mc_sign_en, _, mc_sign_ko, mc_element, mc_degree = get_sign(mc_longitude)
    
    return {
        "asc": (asc_longitude, asc_sign_en, asc_sign_ko, asc_element, asc_degree),
        "mc": (mc_longitude, mc_sign_en, mc_sign_ko, mc_element, mc_degree)
    }


def calculate_fortuna(sun_longitude: float, moon_longitude: float, asc_longitude: float, is_day_chart: bool) -> float:
    """
    포르투나(Part of Fortune) 계산
    
    고전점성술 공식:
    - 낮 차트: ASC + Moon - Sun
    - 밤 차트: ASC + Sun - Moon
    
    Args:
        sun_longitude: 태양의 황도 경도
        moon_longitude: 달의 황도 경도
        asc_longitude: ASC의 황도 경도
        is_day_chart: 낮 차트 여부 (태양이 지평선 위)
        
    Returns:
        포르투나의 황도 경도 (0-360)
    """
    if is_day_chart:
        fortuna = asc_longitude + moon_longitude - sun_longitude
    else:
        fortuna = asc_longitude + sun_longitude - moon_longitude
    
    # 0-360 범위로 정규화
    fortuna = fortuna % 360
    if fortuna < 0:
        fortuna += 360
        
    return fortuna


def is_day_chart(sun_longitude: float, asc_longitude: float) -> bool:
    """
    낮 차트 여부 판별
    
    태양이 ASC(1하우스 cusp) 기준 위쪽 반구(7-12하우스)에 있으면 낮 차트
    """
    # 태양과 ASC의 차이 계산
    diff = (sun_longitude - asc_longitude) % 360
    
    # 태양이 ASC 기준으로 180도 미만 차이면 (desc~asc 사이 = 7~12하우스) 낮
    return diff > 180


def calculate_spirit(sun_longitude: float, moon_longitude: float, asc_longitude: float, is_day_chart: bool) -> float:
    """
    정신의 지점(Lot of Spirit) 계산
    
    고전점성술 공식:
    - 낮 차트: ASC + Sun - Moon
    - 밤 차트: ASC + Moon - Sun
    """
    if is_day_chart:
        spirit = asc_longitude + sun_longitude - moon_longitude
    else:
        spirit = asc_longitude + moon_longitude - sun_longitude
    
    spirit = spirit % 360
    if spirit < 0:
        spirit += 360
        
    return spirit

