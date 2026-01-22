"""
상수 및 매핑 데이터
"""

# 황도대 별자리
ZODIAC_SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

ZODIAC_SYMBOLS = ['♈︎', '♉︎', '♊︎', '♋︎', '♌︎', '♍︎', '♎︎', '♏︎', '♐︎', '♑︎', '♒︎', '♓︎']

SIGN_KO = {
    'Aries': '양자리', 'Taurus': '황소자리', 'Gemini': '쌍둥이자리',
    'Cancer': '게자리', 'Leo': '사자자리', 'Virgo': '처녀자리',
    'Libra': '천칭자리', 'Scorpio': '전갈자리', 'Sagittarius': '사수자리',
    'Capricorn': '염소자리', 'Aquarius': '물병자리', 'Pisces': '물고기자리'
}

# 전통적 룰러십 (헬레니즘 기반)
SIGN_RULERS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury',
    'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury',
    'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter',
    'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}

# 행성 한글명
PLANET_KO = {
    'Sun': '태양', 'Moon': '달', 'Mercury': '수성',
    'Venus': '금성', 'Mars': '화성', 'Jupiter': '목성', 'Saturn': '토성'
}

# 하우스 키워드
HOUSE_KEYWORDS = [
    "자아/신체/성격",      # 1H
    "돈/소유물/가치관",    # 2H
    "형제/소통/여행",      # 3H
    "가정/부모/뿌리",      # 4H
    "자녀/연애/창조성",    # 5H
    "건강/업무/봉사",      # 6H
    "결혼/파트너/계약",    # 7H
    "죽음/유산/변화",      # 8H
    "철학/교육/여행",      # 9H
    "경력/명성/지위",      # 10H
    "친구/희망/공동체",    # 11H
    "은둔/비밀/무의식"     # 12H
]
