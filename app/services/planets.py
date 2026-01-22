import swisseph as swe
from datetime import datetime
import pytz
from typing import Dict, List, Tuple, Optional

# 1. 사인 (Tropical Zodiac) - 원소, 모드, 주인 반영
SIGNS = [
    ("Aries", "♈︎", "양", "fire", "cardinal", "Mars"),
    ("Taurus", "♉︎", "황소", "earth", "fixed", "Venus"),
    ("Gemini", "♊︎", "쌍둥이", "air", "mutable", "Mercury"),
    ("Cancer", "♋︎", "게", "water", "cardinal", "Moon"),
    ("Leo", "♌︎", "사자", "fire", "fixed", "Sun"),
    ("Virgo", "♍︎", "처녀", "earth", "mutable", "Mercury"),
    ("Libra", "♎︎", "천칭", "air", "cardinal", "Venus"),
    ("Scorpio", "♏︎", "전갈", "water", "fixed", "Mars"),
    ("Sagittarius", "♐︎", "사수", "fire", "mutable", "Jupiter"),
    ("Capricorn", "♑︎", "염소", "earth", "cardinal", "Saturn"),
    ("Aquarius", "♒︎", "물병", "air", "fixed", "Saturn"),
    ("Pisces", "♓︎", "물고기", "water", "mutable", "Jupiter")
]

PLANETS = {
    swe.SUN: ("Sun", "☉︎", "태양"),
    swe.MOON: ("Moon", "☽︎", "달"),
    swe.MERCURY: ("Mercury", "☿︎", "수성"),
    swe.VENUS: ("Venus", "♀︎", "금성"),
    swe.MARS: ("Mars", "♂︎", "화성"),
    swe.JUPITER: ("Jupiter", "♃︎", "목성"),
    swe.SATURN: ("Saturn", "♄︎", "토성")
}

# 8. 본질적 위계 데이터
ESSENTIAL_DIGNITIES = {
    "Sun": {"domicile": "Leo", "exaltation": "Aries", "detriment": "Aquarius", "fall": "Libra"},
    "Moon": {"domicile": "Cancer", "exaltation": "Taurus", "detriment": "Capricorn", "fall": "Scorpio"},
    "Mercury": {"domicile": ["Gemini", "Virgo"], "exaltation": "Virgo", "detriment": ["Sagittarius", "Pisces"], "fall": "Pisces"},
    "Venus": {"domicile": ["Taurus", "Libra"], "exaltation": "Pisces", "detriment": ["Scorpio", "Aries"], "fall": "Virgo"},
    "Mars": {"domicile": ["Aries", "Scorpio"], "exaltation": "Capricorn", "detriment": ["Libra", "Taurus"], "fall": "Cancer"},
    "Jupiter": {"domicile": ["Sagittarius", "Pisces"], "exaltation": "Cancer", "detriment": ["Gemini", "Virgo"], "fall": "Capricorn"},
    "Saturn": {"domicile": ["Capricorn", "Aquarius"], "exaltation": "Libra", "detriment": ["Cancer", "Leo"], "fall": "Aries"}
}

# 9. 조이 하우스
JOYS = {
    "Mercury": 1, "Moon": 3, "Venus": 5, "Mars": 6,
    "Sun": 9, "Jupiter": 11, "Saturn": 12
}

def get_sign(longitude: float) -> dict:
    idx = int(longitude / 30) % 12
    degree = longitude % 30
    s = SIGNS[idx]
    return {
        "name": s[0], "symbol": s[1], "name_ko": s[2],
        "element": s[3], "mode": s[4], "ruler": s[5],
        "degree": degree
    }

def format_position(longitude: float, symbol: str) -> str:
    """16° 37' (♎︎) 포맷"""
    deg = int(longitude % 30)
    min_val = int((longitude % 1) * 60)
    return f"{deg:02d}° {min_val:02d}' ({symbol})"

def calculate_planets_core(jd: float, lat: float, lon: float) -> dict:
    results = {}
    planets_list = []
    
    # 기본 행성 계산
    for pid, (name, sym, ko) in PLANETS.items():
        res, _ = swe.calc_ut(jd, pid)
        long = res[0]
        speed = res[3]
        sign_info = get_sign(long)
        
        planets_list.append({
            "id": pid, "name": name, "symbol": sym, "name_ko": ko,
            "position": long, "speed": speed, "retrograde": speed < 0,
            "sign": sign_info["name"], "sign_symbol": sign_info["symbol"], "sign_ko": sign_info["name_ko"],
            "element": sign_info["element"], "degree_f": format_position(long, sign_info["symbol"])
        })
        results[name] = planets_list[-1]

    # 노드 계산
    res_n, _ = swe.calc_ut(jd, swe.MEAN_NODE)
    n_long = res_n[0]
    n_sign = get_sign(n_long)
    s_long = (n_long + 180) % 360
    s_sign = get_sign(s_long)
    
    results["North Node"] = {"name": "North Node", "symbol": "☊︎", "position": n_long, "sign_symbol": n_sign["symbol"], "degree_f": format_position(n_long, n_sign["symbol"])}
    results["South Node"] = {"name": "South Node", "symbol": "☋︎", "position": s_long, "sign_symbol": s_sign["symbol"], "degree_f": format_position(s_long, s_sign["symbol"])}

    return results, planets_list

def get_sect_and_dignity(data: dict, asc_long: float):
    sun = data["Sun"]
    # 2. 섹트 판별 (태양이 ASC-DSC 지평선 기준 위/아래)
    # 간단하게: 낮 차트인지 체크 (실제로는 하우스 시스템으로 체크해야 정확함)
    # 여기서는 하드코딩된 로직보다 하우스 계산 후 처리하는 것이 좋음
    pass

def calculate_lots(asc: float, sun: float, moon: float, is_day: bool):
    """11. 랏(Lot) 계산"""
    if is_day:
        fortuna = (asc + moon - sun) % 360
        spirit = (asc + sun - moon) % 360
    else:
        fortuna = (asc + sun - moon) % 360
        spirit = (asc + moon - sun) % 360
    return fortuna, spirit
