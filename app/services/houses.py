import swisseph as swe
from .planets import get_sign, SIGNS

def calculate_houses_and_points(jd: float, lat: float, lon: float):
    """
    4. 하우스 배치
    홀사인과 포피리 하우스 동시 계산.
    """
    # ASC, MC 등 포인트 계산
    res = swe.houses(jd, lat, lon, b'W') # W: Whole Sign은 커스프만 제공
    cusps = res[0] # 1~12 하우스 커스프
    ascmc = res[1]
    asc_long = ascmc[0]
    mc_long = ascmc[1]
    dsc_long = (asc_long + 180) % 360
    ic_long = (mc_long + 180) % 360

    # 1. Whole Sign Houses (WSH)
    # 1하우스 = ASC가 있는 사인 전체 (0~30도)
    asc_sign_idx = int(asc_long / 30)
    wsh_cusps = []
    for i in range(12):
        wsh_cusps.append(((asc_sign_idx + i) % 12) * 30)

    # 2. Porphyry Houses (Quadrant)
    # ASC~MC 등 주요 앵글 사이를 3등분
    def divide_quadrant(start, end):
        dist = (end - start) % 360
        step = dist / 3
        return [(start + step) % 360, (start + 2*step) % 360]

    porphyry_cusps = [0] * 13
    porphyry_cusps[1] = asc_long
    porphyry_cusps[10] = mc_long
    porphyry_cusps[7] = dsc_long
    porphyry_cusps[4] = ic_long
    
    # 1Q: 10, 11, 12
    q1 = divide_quadrant(mc_long, asc_long) # 10->ASC 사이
    porphyry_cusps[11], porphyry_cusps[12] = q1[0], q1[1]
    
    # 2Q: 1, 2, 3
    q2 = divide_quadrant(asc_long, ic_long)
    porphyry_cusps[2], porphyry_cusps[3] = q2[0], q2[1]

    # 3Q: 4, 5, 6
    q3 = divide_quadrant(ic_long, dsc_long)
    porphyry_cusps[5], porphyry_cusps[6] = q3[0], q3[1]

    # 4Q: 7, 8, 9
    q4 = divide_quadrant(dsc_long, mc_long)
    porphyry_cusps[8], porphyry_cusps[9] = q4[0], q4[1]

    # 하우스 데이터 구조화
    wsh_data = []
    for i in range(1, 13):
        h_idx = i - 1
        start_long = wsh_cusps[h_idx]
        sign_info = get_sign(start_long)
        
        # 하우스 분류 (앵글, 석시던트, 케이던트)
        if i in [1, 4, 7, 10]: cat = "Angular"
        elif i in [2, 5, 8, 11]: cat = "Succedent"
        else: cat = "Cadent"

        # 하우스 길흉
        if i in [1, 5, 10, 11]: fortune = "Good"
        elif i in [6, 8, 12]: fortune = "Bad"
        else: fortune = "Neutral"

        wsh_data.append({
            "number": i,
            "start_long": start_long,
            "sign": sign_info["name"],
            "sign_symbol": sign_info["symbol"],
            "ruler": sign_info["ruler"],
            "category": cat,
            "fortune": fortune
        })

    return {
        "asc": asc_long, "mc": mc_long, "dsc": dsc_long, "ic": ic_long,
        "wsh": wsh_data,
        "porphyry_cusps": porphyry_cusps[1:] 
    }

def get_house_number(long, cusps):
    """주어진 경도가 어떤 하우스에 속하는지 반환"""
    for i in range(12):
        start = cusps[i]
        end = cusps[(i + 1) % 12]
        if start < end:
            if start <= long < end: return i + 1
        else: # 경계가 0도를 지나는 경우
            if long >= start or long < end: return i + 1
    return 1
