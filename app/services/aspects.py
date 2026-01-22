"""애스펙트 계산"""

# 5개 Ptolemaic Aspects
ASPECTS = [
    {"name": "Conjunction", "name_ko": "컨정션", "angle": 0, "orb": 8},
    {"name": "Sextile", "name_ko": "섹스타일", "angle": 60, "orb": 6},
    {"name": "Square", "name_ko": "스퀘어", "angle": 90, "orb": 8},
    {"name": "Trine", "name_ko": "트라인", "angle": 120, "orb": 8},
    {"name": "Opposition", "name_ko": "어포지션", "angle": 180, "orb": 8},
]

# Transit용 딕셔너리 형태 (name -> angle, orb, symbol, name_ko)
MAJOR_ASPECTS = {
    "Conjunction": (0, 8, "☌", "합"),
    "Sextile": (60, 6, "⚹", "육합"),
    "Square": (90, 8, "□", "직각"),
    "Trine": (120, 8, "△", "삼합"),
    "Opposition": (180, 8, "☍", "충")
}


def calculate_aspects(planets: list[dict]) -> list[dict]:
    """
    모든 천체 쌍의 애스펙트 계산
    
    Args:
        planets: 천체 정보 리스트 (각각 position 필드 포함)
        
    Returns:
        애스펙트 정보 리스트
    """
    aspects = []
    
    # 모든 천체 쌍 비교
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            p1 = planets[i]
            p2 = planets[j]
            
            # 두 천체 사이 각도 (0-180)
            diff = abs(p1["position"] - p2["position"])
            if diff > 180:
                diff = 360 - diff
            
            # 각 애스펙트 체크
            for aspect in ASPECTS:
                orb = abs(diff - aspect["angle"])
                
                if orb <= aspect["orb"]:
                    aspects.append({
                        "planet1": p1["name"],
                        "planet1_ko": p1["name_ko"],
                        "planet2": p2["name"],
                        "planet2_ko": p2["name_ko"],
                        "type": aspect["name"],
                        "type_ko": aspect["name_ko"],
                        "angle": aspect["angle"],
                        "orb": round(orb, 2)
                    })
                    break  # 하나의 애스펙트만 적용
    
    return aspects
