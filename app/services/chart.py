from .planets import (
    calculate_planets, 
    calculate_angles, 
    calculate_fortuna,
    calculate_spirit,
    get_triplicity_ruler,
    get_term_ruler,
    get_face_ruler,
    get_planet_dignity,
    get_ruler_planet,
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
    """
    # 1. ASC, MC 계산
    angles = calculate_angles(
        birth_date, birth_time, latitude, longitude, timezone_str
    )
    asc_longitude, asc_sign, asc_sign_ko, asc_element, asc_degree = angles["asc"]
    mc_longitude, mc_sign, mc_sign_ko, mc_element, mc_degree = angles["mc"]
    
    # 2. 천체 위치 계산
    planets = calculate_planets(birth_date, birth_time, timezone_str)
    
    # 3. 주/야 판별 및 5대 품위 계산
    sun_pos = next(p["position"] for p in planets if p["name"] == "Sun")
    moon_pos = next(p["position"] for p in planets if p["name"] == "Moon")
    is_day = is_day_chart(sun_pos, asc_longitude)
    
    for p in planets:
        p["house"] = get_planet_house(p["position"], asc_longitude)
        # 5 Essential Dignities
        dignity_type = get_planet_dignity(p["name"], p["sign"])
        p["dignity"] = dignity_type
        p["triplicity"] = get_triplicity_ruler(p["sign_element"], is_day)
        p["term"] = get_term_ruler(p["sign"], p["degree"])
        p["face"] = get_face_ruler(p["position"])
        p["domicile_ruler"] = get_ruler_planet(p["sign"])
        
    # 4. 하우스 계산 (Whole Sign)
    houses = calculate_houses(asc_longitude)
    
    # 5. 애스펙트 계산
    aspects = calculate_aspects(planets)
    
    # 6. Lots (Fortune & Spirit)
    fortuna_longitude = calculate_fortuna(sun_pos, moon_pos, asc_longitude, is_day)
    fortuna_sign_en, _, fortuna_sign_ko, fortuna_element, fortuna_degree = get_sign(fortuna_longitude)
    fortuna_house = get_planet_house(fortuna_longitude, asc_longitude)

    spirit_longitude = calculate_spirit(sun_pos, moon_pos, asc_longitude, is_day)
    spirit_sign_en, _, spirit_sign_ko, spirit_element, spirit_degree = get_sign(spirit_longitude)
    spirit_house = get_planet_house(spirit_longitude, asc_longitude)
    
    return {
        "planets": planets,
        "houses": houses,
        "aspects": aspects,
        "sect": "Day" if is_day else "Night",
        "ascendant": {
            "sign": asc_sign,
            "sign_ko": asc_sign_ko,
            "element": asc_element,
            "degree": round(asc_degree, 2),
            "degree_formatted": format_degree(asc_degree),
            "position": round(asc_longitude, 4)
        },
        "midheaven": {
            "sign": mc_sign,
            "sign_ko": mc_sign_ko,
            "element": mc_element,
            "degree": round(mc_degree, 2),
            "degree_formatted": format_degree(mc_degree),
            "position": round(mc_longitude, 4)
        },
        "fortuna": {
            "sign": fortuna_sign_en,
            "sign_ko": fortuna_sign_ko,
            "degree": round(fortuna_degree, 2),
            "degree_formatted": format_degree(fortuna_degree),
            "house": fortuna_house,
            "position": round(fortuna_longitude, 4)
        },
        "spirit": {
            "sign": spirit_sign_en,
            "sign_ko": spirit_sign_ko,
            "degree": round(spirit_degree, 2),
            "degree_formatted": format_degree(spirit_degree),
            "house": spirit_house,
            "position": round(spirit_longitude, 4)
        }
    }
