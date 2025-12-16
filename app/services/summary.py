"""AI 프롬프트 생성 - Hellenistic Astrology 전문가 스타일"""

from app.services.planets import get_ruler_planet, ESSENTIAL_DIGNITIES

HOUSE_MEANINGS = [
    "생명, 자아, 신체, 외모",                          # 1H - Horoskopos
    "생계, 재물, 소유, 거래",                          # 2H - Gate of Hades
    "형제, 이동, 친척, 꿈",                            # 3H - Goddess
    "가정, 부모, 부동산, 뿌리, 노년",                   # 4H - Subterraneous
    "자녀, 쾌락, 우정, 창조",                          # 5H - Good Fortune
    "질병, 노동, 하인, 작은 동물",                      # 6H - Bad Fortune
    "결혼, 배우자, 파트너십, 공개된 적",                 # 7H - Descendant
    "죽음, 유산, 타인의 자원, 법적 문제",                # 8H - Idle Place (오컬트 X)
    "철학, 종교, 여행, 점술, 신탁, 신비로운 사항",        # 9H - God (오컬트 O)
    "직업, 명예, 사회적 지위, 행동",                    # 10H - Midheaven
    "친구, 희망, 후원자, 선물",                        # 11H - Good Spirit
    "외국, 적대, 고립, 숨겨진 적, 위험"                  # 12H - Bad Spirit (업보 X)
]

ASPECT_MEANINGS = {
    "Conjunction": "강한 결합과 융합",
    "Sextile": "기회와 협력 (부드러운 조화)",
    "Square": "긴장과 갈등, 행동을 유발하는 도전",
    "Trine": "자연스러운 흐름과 행운, 재능",
    "Opposition": "대립과 타협, 긴장 관계"
}

DIGNITY_LABELS = {
    "domicile": "Domicile (매우 강함)",
    "exaltation": "Exaltation (강화됨)",
    "detriment": "Detriment (약화됨)",
    "fall": "Fall (매우 약함)",
    "peregrine": "Peregrine (중립)"
}

# 행성의 본질적 성질 (Sect 무관)
BENEFICS = {"Venus", "Jupiter"}
MALEFICS = {"Mars", "Saturn"}
LUMINARIES = {"Sun", "Moon"}
NEUTRAL = {"Mercury"}  # Mercury는 함께 있는 행성에 따라 결정


def get_sect_status(planet_name: str, is_day_chart: bool) -> str:
    """
    Sect에 따른 행성의 길/흉 상태 판정 (헬레니즘 기준)
    
    Day Chart: Sun=Sect Light, Jupiter=Benefic of Sect, Saturn=Malefic of Sect (건설적)
               Venus=Benefic out of Sect, Mars=Malefic out of Sect (파괴적)
    Night Chart: Moon=Sect Light, Venus=Benefic of Sect, Mars=Malefic of Sect (건설적)
                 Jupiter=Benefic out of Sect, Saturn=Malefic out of Sect (파괴적)
    """
    if is_day_chart:
        if planet_name == "Sun":
            return "Sect Light (주도 행성)"
        elif planet_name == "Jupiter":
            return "Benefic of Sect (강한 길성)"
        elif planet_name == "Saturn":
            return "Malefic of Sect (건설적 흉성)"
        elif planet_name == "Venus":
            return "Benefic out of Sect (약한 길성)"
        elif planet_name == "Mars":
            return "Malefic out of Sect (파괴적 흉성)"
        elif planet_name == "Moon":
            return "Luminary (보조광)"
        else:
            return "Neutral"
    else:  # Night Chart
        if planet_name == "Moon":
            return "Sect Light (주도 행성)"
        elif planet_name == "Venus":
            return "Benefic of Sect (강한 길성)"
        elif planet_name == "Mars":
            return "Malefic of Sect (건설적 흉성)"
        elif planet_name == "Jupiter":
            return "Benefic out of Sect (약한 길성)"
        elif planet_name == "Saturn":
            return "Malefic out of Sect (파괴적 흉성)"
        elif planet_name == "Sun":
            return "Luminary (보조광)"
        else:
            return "Neutral"


def get_conjunction_quality(planet1: str, planet2: str) -> str:
    """
    Conjunction의 길/흉 판정 (헬레니즘 기준)
    
    길성+길성 = Benefic
    흉성+흉성 = Malefic  
    혼합 = Mixed
    """
    def get_nature(p):
        if p in BENEFICS:
            return "benefic"
        elif p in MALEFICS:
            return "malefic"
        else:
            return "neutral"  # Luminaries, Mercury
    
    n1 = get_nature(planet1)
    n2 = get_nature(planet2)
    
    if n1 == "benefic" and n2 == "benefic":
        return "Benefic (길)"
    elif n1 == "malefic" and n2 == "malefic":
        return "Malefic (흉)"
    elif n1 == "neutral" or n2 == "neutral":
        return "Neutral (중립)"
    else:
        return "Mixed (혼합)"


def get_planet_dignity(planet_name: str, sign_name: str) -> str:
    """행성의 Essential Dignity 판별"""
    dignity_data = ESSENTIAL_DIGNITIES.get(planet_name, {})
    
    if sign_name in dignity_data.get('domicile', []):
        return DIGNITY_LABELS["domicile"]
    if sign_name in dignity_data.get('exaltation', []):
        return DIGNITY_LABELS["exaltation"]
    if sign_name in dignity_data.get('detriment', []):
        return DIGNITY_LABELS["detriment"]
    if sign_name in dignity_data.get('fall', []):
        return DIGNITY_LABELS["fall"]
    return DIGNITY_LABELS["peregrine"]



def generate_ai_summary(data: dict, name: str = "Unknown", gender: str = "unknown", 
                        birth_date: str = "", birth_time: str = "", place_name: str = "") -> str:
    """
    네이탈 차트 데이터를 기반으로 AI 프롬프트 생성.
    결정론적/구조적 관점의 Hellenistic 분석을 유도하는 형식.
    """
    lines = []
    
    # === SYSTEM HEADER ===
    lines.append("=== SYSTEM: Hellenistic Astrology / Classical 7 Planets Only ===")
    lines.append("(천왕성, 해왕성, 명왕성, 키론 등 현대 천체 절대 언급 금지)")
    lines.append("")
    
    # [1] 핵심 지표
    sect = data.get('sect', 'Unknown')
    is_day = sect == 'Day'
    asc = data['ascendant']
    
    # Chart Ruler 찾기
    asc_sign_en = asc['sign']
    chart_ruler_name = get_ruler_planet(asc_sign_en)
    chart_ruler = next((p for p in data['planets'] if p['name'] == chart_ruler_name), None)
    chart_ruler_info = "정보 없음"
    if chart_ruler:
        dignity = get_planet_dignity(chart_ruler['name'], chart_ruler['sign'])
        chart_ruler_info = f"{chart_ruler['name_ko']} in {chart_ruler['sign_ko']} {chart_ruler['house']}H [{dignity}]"
    
    lines.append("[1] 핵심 지표 (Primary Indicators)")
    lines.append(f"- Sect: {'낮 차트 (Day Chart)' if is_day else '밤 차트 (Night Chart)'}")
    lines.append(f"- 상승궁(ASC): {asc['sign_ko']} {asc['degree_formatted']}")
    lines.append(f"- 차트 룰러: {chart_ruler_info}")
    lines.append(f"- MC(중천): {data['midheaven']['sign_ko']} {data['midheaven']['degree_formatted']}")
    lines.append(f"- 포르투나: {data['fortuna']['sign_ko']} {data['fortuna']['degree_formatted']} ({data['fortuna']['house']}H)")
    lines.append("")
    
    # [2] 행성 배치 + Sect Status
    lines.append("[2] 행성 배치 (Planetary Positions with Dignity & Sect)")
    for p in data['planets']:
        symbol = p.get('symbol', '')
        dignity = get_planet_dignity(p['name'], p['sign'])
        sect_status = get_sect_status(p['name'], is_day)
        retro = " (R)" if p.get('retrograde') else ""
        lines.append(f"- {symbol} {p['name_ko']}: {p['sign_ko']} {p['degree_formatted']}{retro} / {p['house']}H")
        lines.append(f"    Dignity: {dignity} | Sect: {sect_status}")
    lines.append("")
    
    # [3] 하우스별 상세
    lines.append("[3] 하우스별 상세 구조 (Whole Sign Houses)")
    
    # 하우스별 행성 맵핑
    house_planets = {i: [] for i in range(1, 13)}
    for p in data['planets']:
        house_planets[p['house']].append(p['name_ko'])
    
    for house in data['houses']:
        num = house['number']
        sign_ko = house['sign_ko']
        sign_en = house['sign']
        
        # Ruler
        ruler_name = get_ruler_planet(sign_en)
        ruler_data = next((p for p in data['planets'] if p['name'] == ruler_name), None)
        
        ruler_str = "정보 없음"
        ruler_dignity = ""
        if ruler_data:
            ruler_dignity = get_planet_dignity(ruler_data['name'], ruler_data['sign'])
            ruler_str = f"{ruler_data['name_ko']} in {ruler_data['sign_ko']} {ruler_data['house']}H [{ruler_dignity}]"
        
        occupants = house_planets.get(num, [])
        occupants_str = ", ".join(occupants) if occupants else "없음"
        
        lines.append(f"### {num}H ({sign_ko})")
        lines.append(f"- 주제: {HOUSE_MEANINGS[num - 1]}")
        lines.append(f"- 내재 행성: {occupants_str}")
        lines.append(f"- 룰러: {ruler_str}")
        
        # 빈 하우스 가이드
        if not occupants and ruler_data:
            lines.append(f"  -> (Guide): 빈 하우스. 룰러 '{ruler_data['name_ko']}'의 상태({ruler_data['sign_ko']}, {ruler_data['house']}H)를 추적하여 해석.")
        lines.append("")
    
    # [4] 주요 애스펙트
    lines.append("[4] 주요 애스펙트 (Aspects)")
    if data['aspects']:
        for asp in data['aspects']:
            aspect_type = asp['type']
            meaning = ASPECT_MEANINGS.get(aspect_type, aspect_type)
            
            # 길/흉 판정
            if aspect_type in ["Trine", "Sextile"]:
                nature = "Soft (길각)"
            elif aspect_type in ["Square", "Opposition"]:
                nature = "Hard (흉각)"
            elif aspect_type == "Conjunction":
                # Conjunction은 행성 조합에 따라 판정
                nature = get_conjunction_quality(asp['planet1'], asp['planet2'])
            else:
                nature = "Neutral"
            
            lines.append(f"- {aspect_type} [{nature}]: {asp['planet1']} - {asp['planet2']} (orb {asp['orb']:.2f}°)")
    else:
        lines.append("- 주요 메이저 애스펙트 없음")
    lines.append("")
    
    # === AI 해석 지침 ===
    lines.append("---")
    lines.append("")
    lines.append("!!! AI 해석 지침 !!!")
    lines.append("1. 위 데이터에 명시된 7행성만 사용. 현대 천체(천왕성/해왕성/명왕성) 절대 금지.")
    lines.append("2. Dignity(품위)를 참고하여 행성의 길흉 상태를 반영.")
    lines.append("3. Sect(주/야)를 고려하여 길성/흉성 판단 (Day: 태양/목성 유리, Night: 달/금성 유리).")
    lines.append("4. 빈 하우스는 반드시 룰러를 추적하여 통변.")
    lines.append("5. 심리적 위로보다 현실적 사건과 결정론적 뉘앙스 유지.")
    lines.append("6. 결과는 반드시 한국어로 작성.")
    lines.append("")
    lines.append(f"[내담자 정보] 이름: {name} / 성별: {gender} / 생년월일: {birth_date} / 출생시간: {birth_time} / 출생지: {place_name or 'Unknown'}")
    
    return "\n".join(lines)
