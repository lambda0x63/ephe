from app.services.planets import get_ruler_planet, get_planet_dignity, get_dignity_description

HOUSE_MEANINGS = [
    "자아, 생명력, 성격, 외모",
    "재물, 소유, 수입",
    "형제, 커뮤니케이션, 이동",
    "가정, 부모(아버지), 부동산, 뿌리",
    "창조, 자녀, 연애, 즐거움",
    "건강, 노동, 의무, 작은 동물",
    "결혼, 배우자, 파트너십, 공개된 적",
    "죽음, 유산, 타인의 돈, 오컬트",
    "철학, 종교, 고등교육, 장거리 여행",
    "직업, 명예, 사회적 지위, 어머니",
    "친구, 희망, 그룹 활동, 후원자",
    "고립, 숨겨진 적, 무의식, 업보"
]

# 애스펙트 길흉 분류
ASPECT_NATURE = {
    "Conjunction": "Neutral",
    "Sextile": "Soft (길각)",
    "Trine": "Soft (길각)",
    "Square": "Hard (흉각)",
    "Opposition": "Hard (흉각)"
}


def generate_ai_summary(chart_data: dict) -> str:
    """
    AI 간명용 구조화된 텍스트 리포트 생성
    (Hellenistic / Classical 7 Planets Only)
    """
    lines = []
    
    # ========== 시스템 지침 (상단) ==========
    lines.append("=== SYSTEM: Hellenistic Astrology / Classical 7 Planets Only ===")
    lines.append("(천왕성, 해왕성, 명왕성, 키론 등 현대 천체 절대 언급 금지)")
    lines.append("")
    
    # ========== 헤더 ==========
    asc_sign = chart_data['ascendant']['sign_ko']
    asc_degree = chart_data['ascendant']['degree_formatted']
    asc_sign_en = chart_data['ascendant']['sign']
    
    chart_ruler_name_en = get_ruler_planet(asc_sign_en)
    chart_ruler = next((p for p in chart_data['planets'] if p['name'] == chart_ruler_name_en), None)
    
    # Sect (주/야)
    sect = chart_data.get('sect', 'Unknown')
    sect_ko = "낮 차트 (Day Chart)" if sect == "Day" else "밤 차트 (Night Chart)"
    
    lines.append("[1] 핵심 지표 (Primary Indicators)")
    lines.append(f"- Sect: {sect_ko}")
    lines.append(f"- 상승궁(ASC): {asc_sign} {asc_degree}")
    if chart_ruler:
        ruler_dignity = get_planet_dignity(chart_ruler['name'], chart_ruler['sign'])
        ruler_dignity_desc = get_dignity_description(ruler_dignity)
        lines.append(f"- 차트 룰러: {chart_ruler['name_ko']} in {chart_ruler['sign_ko']} {chart_ruler['house']}H [{ruler_dignity_desc}]")
    lines.append(f"- MC(중천): {chart_data['midheaven']['sign_ko']} {chart_data['midheaven']['degree_formatted']}")
    lines.append(f"- 포르투나: {chart_data['fortuna']['sign_ko']} {chart_data['fortuna']['degree_formatted']} ({chart_data['fortuna']['house']}H)")
    lines.append("")

    # ========== 행성 배치 (Dignity 포함) ==========
    lines.append("[2] 행성 배치 (Planetary Positions with Dignity)")
    for p in chart_data['planets']:
        retro = " [R]" if p['retrograde'] else ""
        dignity = get_planet_dignity(p['name'], p['sign'])
        dignity_desc = get_dignity_description(dignity)
        lines.append(f"- {p['name_ko']}: {p['sign_ko']} {p['degree_formatted']}{retro} / {p['house']}H [{dignity_desc}]")
    lines.append("")

    # ========== 하우스별 상세 ==========
    lines.append("[3] 하우스별 상세 구조 (Whole Sign Houses)")
    
    house_planets = {i: [] for i in range(1, 13)}
    for p in chart_data['planets']:
        house_planets[p['house']].append(p['name_ko'])
    
    for house in chart_data['houses']:
        num = house['number']
        sign = house['sign_ko']
        sign_en = house['sign']
        
        ruler_en = get_ruler_planet(sign_en)
        ruler_data = next((p for p in chart_data['planets'] if p['name'] == ruler_en), None)
        if ruler_data:
            ruler_dignity = get_planet_dignity(ruler_data['name'], ruler_data['sign'])
            ruler_info = f"{ruler_data['name_ko']} in {ruler_data['sign_ko']} {ruler_data['house']}H [{ruler_dignity}]"
        else:
            ruler_info = "Unknown"
        
        occupants = house_planets.get(num, [])
        occupants_str = ", ".join(occupants) if occupants else "없음"
        
        lines.append(f"### {num}H ({sign})")
        lines.append(f"- 주제: {HOUSE_MEANINGS[num-1]}")
        lines.append(f"- 내재 행성: {occupants_str}")
        lines.append(f"- 룰러: {ruler_info}")
        if not occupants and ruler_data:
            lines.append(f"  -> (Guide): 빈 하우스. 룰러 '{ruler_data['name_ko']}'의 상태({ruler_data['sign_ko']}, {ruler_data['house']}H)를 추적하여 해석.")
        lines.append("")

    # ========== 애스펙트 (길흉 표기) ==========
    lines.append("[4] 주요 애스펙트 (Aspects)")
    for aspect in chart_data['aspects']:
        orb = f"{aspect['orb']}°"
        nature = ASPECT_NATURE.get(aspect['type'], "Neutral")
        lines.append(f"- {aspect['type_ko']} [{nature}]: {aspect['planet1_ko']} - {aspect['planet2_ko']} (orb {orb})")
    lines.append("")

    # ========== 시스템 지침 (하단) ==========
    lines.append("---")
    lines.append("!!! AI 해석 지침 !!!")
    lines.append("1. 위 데이터에 명시된 7행성만 사용. 현대 천체(천왕성/해왕성/명왕성) 절대 금지.")
    lines.append("2. Dignity(품위)를 참고하여 행성의 길흉 상태를 반영.")
    lines.append("3. Sect(주/야)를 고려하여 길성/흉성 판단 (Day: 태양/목성 유리, Night: 달/금성 유리).")
    lines.append("4. 빈 하우스는 반드시 룰러를 추적하여 통변.")
    lines.append("5. 심리적 위로보다 현실적 사건과 결정론적 뉘앙스 유지.")

    report = "\n".join(lines)
    return report
