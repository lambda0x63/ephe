from app.services.planets import get_ruler_planet, ESSENTIAL_DIGNITIES

HOUSE_MEANINGS = [
    "생명, 자아, 외모, 활력 (1H)",
    "소유, 재물, 가치관 (2H)",
    "형제, 커뮤니케이션, 단거리 여행, 학습 (3H)",
    "가정, 부모, 뿌리, 노년 (4H)",
    "창조, 유흥, 자녀, 로맨스 (5H)",
    "노동, 질병, 의무, 반려동물 (6H)",
    "결혼, 파트너십, 공개된 적 (7H)",
    "타인의 돈, 죽음, 오컬트, 유산 (8H)",
    "철학, 종교, 장거리 여행, 고등교육 (9H)",
    "직업, 명예, 사회적 지위, 권위 (10H)",
    "친구, 소망, 그룹 활동, 행운 (11H)",
    "고립, 숨겨진 적, 무의식, 자선 (12H)"
]

ASPECT_MEANINGS = {
    "Conjunction": "강한 결합과 융합",
    "Sextile": "기회와 협력 (부드러운 조화)",
    "Square": "긴장과 갈등, 행동을 유발하는 도전",
    "Trine": "자연스러운 흐름과 행운, 재능",
    "Opposition": "대립과 타협, 긴장 관계"
}

def get_planet_dignity(planet_name, sign_name):
    """행성의 본질적 위계(Essential Dignity) 판별"""
    # planets.py의 구조: { "Sun": { "domicile": ["Leo"], ... } }
    dignity_data = ESSENTIAL_DIGNITIES.get(planet_name, {})
    
    if sign_name in dignity_data.get('domicile', []):
        return "Domicile (Ruler) - 매우 강력함"
    if sign_name in dignity_data.get('exaltation', []):
        return "Exaltation - 고귀하고 강력함"
    if sign_name in dignity_data.get('detriment', []):
        return "Detriment - 힘을 쓰기 어려움"
    if sign_name in dignity_data.get('fall', []):
        return "Fall - 매우 약하고 불편함"
        
    return "Peregrine - 중립적"

def generate_ai_summary(data, name="Unknown", gender="unknown", birth_date="", birth_time="", place_name=""):
    """
    네이탈 차트 데이터를 기반으로 AI(ChatGPT/Claude)가 해석할 수 있는
    상세한 프롬프트 텍스트를 생성합니다.
    """
    
    # 1. 헤더 및 System Instructions (강력한 지침 복원)
    prompt_lines = [
        "## System: Role & Context",
        "You are an expert Hellenistic Astrologer. Analyze the following natal chart data using Whole Sign Houses.",
        "**Strict Guidelines:**",
        "1. **Methodology**: Use strictly Hellenistic techniques. Focus on Essential Dignities (Domicile, Exaltation, Detriment, Fall), House rulers, and Sect.",
        "2. **Exclusions**: Do NOT focus on modern outer planets (Uranus, Neptune, Pluto) as primary significators.",
        "3. **Structure**: Provide a comprehensive reading covering Life Purpose (Sun), Emotions/Body (Moon), Communication (Mercury), Relationships (Venus), Action (Mars), Wisdom (Jupiter), and Challenges (Saturn).",
        "4. **Tone**: Be insightful, empathetic, yet clear and professional.",
        "5. **Language**: Write the FINAL reading IN KOREAN (결과는 반드시 한국어로 작성하십시오).",
        "",
        "## 1. Querent Information (내담자 정보)",
        f"- Name: {name}",
        f"- Gender: {gender} (Consider gender context if relevant to traditional interpretations, but apply modern flexibility)",
        f"- Birth Date: {birth_date}",
        f"- Birth Time: {birth_time}",
        f"- Place: {place_name or 'Unknown'}",
        "",
        "## 2. Chart Data Report",
        ""
    ]

    # 2. Ascendant & Sect
    sect = data.get('sect', 'Unknown')
    prompt_lines.append(f"### [1] 기본 구조")
    prompt_lines.append(f"- Ascendant (상승궁): {data['ascendant']['sign_ko']} {data['ascendant']['degree_formatted']}")
    prompt_lines.append(f"- Chart Sect: {sect} (낮의 차트인가 밤의 차트인가?)")
    if sect == "Day Chart":
        prompt_lines.append("  -> Key Planets: Sun(빛), Jupiter(협조), Saturn(도전)")
    else:
        prompt_lines.append("  -> Key Planets: Moon(빛), Venus(협조), Mars(도전)")
    prompt_lines.append("")

    # 3. 행성 배치
    prompt_lines.append("### [2] 행성 배치 및 위계 (Planets & Dignities)")
    for p in data['planets']:
        retro = " (Retrograde - 역행)" if p['retrograde'] else ""
        dignity = get_planet_dignity(p['name'], p['sign'])
        # symbol 사용 가능 시 사용
        symbol = p.get('symbol', '')
        prompt_lines.append(f"- {symbol} {p['name_ko']}: {p['sign_ko']} {p['degree_formatted']}{retro} / {p['house']}H [{dignity}]")
    prompt_lines.append("")

    # 4. 하우스별 상세
    prompt_lines.append("### [3] 하우스별 상세 구조 (Whole Sign Houses)")
    
    house_planets = {i: [] for i in range(1, 13)}
    for p in data['planets']:
        house_planets[p['house']].append(p['name_ko'])
    
    for house in data['houses']:
        num = house['number']
        sign = house['sign_ko']
        sign_en = house['sign']
        
        # Ruler Info
        ruler_en = get_ruler_planet(sign_en)
        ruler_data = next((p for p in data['planets'] if p['name'] == ruler_en), None)
        
        ruler_info = "정보 없음"
        if ruler_data:
            ruler_dignity = get_planet_dignity(ruler_data['name'], ruler_data['sign'])
            ruler_info = f"{ruler_data['name_ko']} in {ruler_data['sign_ko']} {ruler_data['house']}H [{ruler_dignity}]"

        occupants = house_planets.get(num, [])
        occupants_str = ", ".join(occupants) if occupants else "없음"
        
        prompt_lines.append(f"#### {num}H ({sign})")
        prompt_lines.append(f"- 주제: {HOUSE_MEANINGS[num-1]}")
        prompt_lines.append(f"- 내재 행성: {occupants_str}")
        prompt_lines.append(f"- 하우스 룰러: {ruler_info}")
        if not occupants and ruler_data:
            # 빈 하우스일 때 룰러 해석 가이드
            prompt_lines.append(f"  -> (Tip): 빈 하우스입니다. 이 하우스의 문제는 주인 행성인 '{ruler_data['name_ko']}'의 상태를 보고 판단하세요.")
        prompt_lines.append("")

    # 5. 애스펙트
    prompt_lines.append("### [4] 주요 애스펙트 (Major Aspects)")
    if data['aspects']:
        for asp in data['aspects']:
            # P1 (orb) Aspect P2
            meaning = ASPECT_MEANINGS.get(asp['type'], asp['type'])
            prompt_lines.append(f"- {asp['planet1']} {asp['type']} {asp['planet2']} (Orb: {asp['orb']:.1f}°)")
            prompt_lines.append(f"  -> 의미: {meaning}")
    else:
        prompt_lines.append("- 주요 메이저 애스펙트 없음")
    prompt_lines.append("")

    return "\n".join(prompt_lines)
