import swisseph as swe
from datetime import datetime
import pytz

from .planets import calculate_planets_core, calculate_lots, ESSENTIAL_DIGNITIES, JOYS, format_position, get_sign
from .houses import calculate_houses_and_points, get_house_number
from .aspects import calculate_aspects

async def calculate_natal_chart(name: str, birth_date: str, birth_time: str, lat: float, lon: float, tz_str: str):
    """
    네이탈 차트 종합 계산 (비즈니스 로직 적용)
    """
    # 1. 시간 계산
    dt_str = f"{birth_date} {birth_time}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    local_tz = pytz.timezone(tz_str)
    local_dt = local_tz.localize(dt)
    utc_dt = local_dt.astimezone(pytz.UTC)
    
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0)
    
    # 2. 기초 천문 계산
    planets_raw, planets_list = calculate_planets_core(jd, lat, lon)
    house_pts = calculate_houses_and_points(jd, lat, lon)
    
    asc = house_pts["asc"]
    wsh_cusps = [h["start_long"] for h in house_pts["wsh"]]
    porphyry_cusps = house_pts["porphyry_cusps"]

    # 3. 섹트(Sect) 판별
    # 태양의 밤/낮 여부 (ASC-DSC 지평선 기준)
    sun_long = planets_raw["Sun"]["position"]
    # 하우스 시스템에서 태양이 7~12하우스에 있으면 낮(Day)
    sun_wsh = get_house_number(sun_long, wsh_cusps)
    is_day = sun_wsh >= 7
    
    # 4. 행성별 세부 상태 계산
    processed_planets = []
    for p in planets_list:
        p_name = p["name"]
        p_long = p["position"]
        
        # 하우스 위치 (홀사인 & 포피리)
        wsh = get_house_number(p_long, wsh_cusps)
        porphyry = get_house_number(p_long, porphyry_cusps)
        
        # 행성 강약 (하우스 분류)
        h_info = house_pts["wsh"][wsh-1]
        p_cat = h_info["category"] # Angular, Succedent, Cadent
        
        # 섹트 일치 여부
        in_sect = False
        if is_day:
            if p_name in ["Sun", "Jupiter", "Saturn"]: in_sect = True
        else:
            if p_name in ["Moon", "Venus", "Mars"]: in_sect = True
        
        # 6. 태양과의 관계 (컴버스트 등)
        sun_rel = "Free"
        dist = abs(p_long - sun_long)
        if dist > 180: dist = 360 - dist
        
        if p_name != "Sun":
            if dist <= 0.28: sun_rel = "Cazimi" # 17분
            elif dist <= 7.5: sun_rel = "Combust"
            elif dist <= 15: sun_rel = "Under Sunbeams"
            elif dist <= 20: sun_rel = "Phasis"
            
        # 8. 본질적 위계 (Domicile, Exaltation 등)
        dignity = "None"
        sign_name = p["sign"]
        if p_name in ESSENTIAL_DIGNITIES:
            d = ESSENTIAL_DIGNITIES[p_name]
            if isinstance(d["domicile"], list):
                if sign_name in d["domicile"]: dignity = "Domicile"
            elif sign_name == d["domicile"]: dignity = "Domicile"
            
            if sign_name == d.get("exaltation"): dignity = "Exaltation"
            
            # Detriment/Fall
            if isinstance(d.get("detriment"), list):
                if sign_name in d["detriment"]: dignity = "Detriment"
            elif sign_name == d.get("detriment"): dignity = "Detriment"
            
            if sign_name == d.get("fall"): dignity = "Fall"

        # 9. 조이 하우스
        is_joy = JOYS.get(p_name) == wsh

        processed_planets.append({
            **p,
            "wsh": wsh,
            "porphyry": porphyry,
            "category": p_cat,
            "sun_relation": sun_rel,
            "dignity": dignity,
            "in_sect": in_sect,
            "is_joy": is_joy
        })

    # 11. 랏(Lot) 계산
    moon_long = planets_raw["Moon"]["position"]
    f_long, s_long = calculate_lots(asc, sun_long, moon_long, is_day)
    f_sign = get_sign(f_long)
    s_sign = get_sign(s_long)
    
    lots = {
        "Fortuna": {"name": "Fortuna", "symbol": "⊗", "position": f_long, "wsh": get_house_number(f_long, wsh_cusps), "degree_f": format_position(f_long, f_sign["symbol"]), "sign_symbol": f_sign["symbol"]},
        "Spirit": {"name": "Spirit", "symbol": "⊕", "position": s_long, "wsh": get_house_number(s_long, wsh_cusps), "degree_f": format_position(s_long, s_sign["symbol"]), "sign_symbol": s_sign["symbol"]}
    }

    # 12. 애스펙트
    aspects = calculate_aspects(processed_planets)

    return {
        "meta": {"name": name, "date": birth_date, "time": birth_time, "is_day": is_day},
        "planets": processed_planets,
        "houses": house_pts["wsh"],
        "porphyry_cusps": house_pts["porphyry_cusps"],
        "angles": {
            "asc": {"position": asc, "degree_f": format_position(asc, get_sign(asc)["symbol"]), "symbol": get_sign(asc)["symbol"]},
            "dsc": {
                "position": (asc + 180) % 360, 
                "degree_f": format_position((asc + 180) % 360, get_sign((asc + 180) % 360)["symbol"]), 
                "symbol": get_sign((asc + 180) % 360)["symbol"]
            },
            "mc": {
                "position": house_pts["mc"], 
                "degree_f": format_position(house_pts["mc"], get_sign(house_pts["mc"])["symbol"]), 
                "symbol": get_sign(house_pts["mc"])["symbol"],
                "wsh": get_house_number(house_pts["mc"], wsh_cusps),
                "porphyry": 10
            },
            "ic": {
                "position": (house_pts["mc"] + 180) % 360, 
                "degree_f": format_position((house_pts["mc"] + 180) % 360, get_sign((house_pts["mc"] + 180) % 360)["symbol"]), 
                "symbol": get_sign((house_pts["mc"] + 180) % 360)["symbol"],
                "wsh": get_house_number((house_pts["mc"] + 180) % 360, wsh_cusps),
                "porphyry": 4
            }
        },
        "lots": lots,
        "aspects": aspects
    }
