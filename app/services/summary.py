from app.services.planets import get_ruler_planet

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

def generate_ai_summary(chart_data: dict) -> str:
    """
    AI 간명용 구조화된 텍스트 리포트 생성
    """
    lines = []
    
    # 1. 헤더 (상승궁 & 차트 룰러)
    asc_sign = chart_data['ascendant']['sign_ko']
    asc_degree = chart_data['ascendant']['degree_formatted']
    asc_sign_en = chart_data['ascendant']['sign']
    
    chart_ruler_name_en = get_ruler_planet(asc_sign_en)
    # 룰러 행성 정보 찾기
    chart_ruler = next((p for p in chart_data['planets'] if p['name'] == chart_ruler_name_en), None)
    
    lines.append("=== 🏛️ 고전 점성술(Hellenistic) 차트 분석 데이터 ===")
    lines.append("")
    lines.append("[1] 핵심 지표 (Primary Angles & Ruler)")
    lines.append(f"- 상승궁(ASC): {asc_sign} {asc_degree}")
    if chart_ruler:
        lines.append(f"- 차트 룰러: {chart_ruler['name_ko']} (in {chart_ruler['sign_ko']}, {chart_ruler['house']} house)")
    lines.append(f"- MC(중천): {chart_data['midheaven']['sign_ko']} {chart_data['midheaven']['degree_formatted']}")
    lines.append(f"- 포르투나(Lot of Fortune): {chart_data['fortuna']['sign_ko']} {chart_data['fortuna']['degree_formatted']}")
    lines.append("")

    lines.append("[2] 행성 배치 (Planetary Positions)")
    for p in chart_data['planets']:
        retro = " [역행]" if p['retrograde'] else ""
        lines.append(f"- {p['name_ko']}: {p['sign_ko']} {p['degree_formatted']}{retro} (House {p['house']})")
    lines.append("")

    lines.append("[3] 하우스별 상세 구조 (Whole Sign Houses)")
    
    # 하우스별 거주 행성 매핑
    house_planets = {i: [] for i in range(1, 13)}
    for p in chart_data['planets']:
        house_planets[p['house']].append(p['name_ko'])
    
    for house in chart_data['houses']:
        num = house['number']
        sign = house['sign_ko']
        sign_en = house['sign']
        
        # 하우스 룰러
        ruler_en = get_ruler_planet(sign_en)
        ruler_data = next((p for p in chart_data['planets'] if p['name'] == ruler_en), None)
        ruler_info = f"{ruler_data['name_ko']} (in {ruler_data['sign_ko']} {ruler_data['house']}H)" if ruler_data else "Unknown"
        
        # 거주 행성
        occupants = house_planets.get(num, [])
        occupants_str = ", ".join(occupants) if occupants else "없음"
        
        lines.append(f"### {num}하우스 ({sign})")
        lines.append(f"- 주제: {HOUSE_MEANINGS[num-1]}")
        lines.append(f"- 내재 행성: {occupants_str}")
        lines.append(f"- 하우스 룰러: {ruler_info}")
        if not occupants:
            lines.append(f"  -> (Guide): 이 하우스는 비어 있으므로, 룰러인 '{ruler_data['name_ko']}'의 상태를 중심으로 해석하십시오.")
        lines.append("")

    lines.append("[4] 주요 애스펙트 (Aspects)")
    for aspect in chart_data['aspects']:
        orb = f"{aspect['orb']}°"
        lines.append(f"- {aspect['type_ko']}: {aspect['planet1_ko']} ↔ {aspect['planet2_ko']} (오차 {orb})")

    lines.append("")
    lines.append("---")
    lines.append("!!! AI 해석 지침 (Strict Guidelines for AI) !!!")
    lines.append("1. [중요] 오직 '고전 7행성'만 사용하십시오. (천왕성, 해왕성, 명왕성, 키론 등 현대 천체 절대 언급 금지)")
    lines.append("2. 심리적 성향보다 '현실적 사건'과 '길흉' 위주로 해석하십시오.")
    lines.append("3. 하우스가 비어있을 경우, 반드시 제공된 가이드에 따라 '하우스 룰러'의 상태를 추적하여 통변하십시오.")
    lines.append("4. 현대 점성술의 심리적 위로보다는, 고전의 결정론적이고 운명론적인 뉘앙스를 유지하십시오.")

    report = "\n".join(lines)
    return report
