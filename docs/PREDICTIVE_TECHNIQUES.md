# 헬레니즘 점성술 예측 기법 - 구현 가이드

## 현재 구현 상태

| 기법 | 상태 | 우선순위 |
|------|------|----------|
| ✅ Essential Dignities | 완료 | - |
| ✅ Sect 분류 | 완료 | - |
| ✅ House Rulers | 완료 | - |
| ✅ Annual Profections | 완료 | - |
| ❌ Decennials | 미구현 | 중간 |
| ❌ Zodiacal Releasing | 미구현 | 낮음 |
| ❌ Transits | 미구현 | 중간 |

---

## 미구현 기법 상세

### 1. Decennials (10년 9개월 주기)

**목적**: 인생의 큰 장(章)을 파악

**원리**:
- 전체 인생을 7개 행성이 순서대로 지배
- 각 행성의 지배 기간 = 129개월 (10년 9개월)
- Day Chart: Sun → Venus → Mercury → Mars → Jupiter → Saturn → Moon
- Night Chart: Moon → Venus → Sun → Mercury → Mars → Jupiter → Saturn

**구현 난이도**: 🟡 중간

**구현 방법**:
```python
PLANET_PERIODS = {
    'Sun': 19, 'Moon': 25, 'Mercury': 20, 
    'Venus': 8, 'Mars': 15, 'Jupiter': 12, 'Saturn': 30
}
# 총합: 129개월

def calculate_decennials(birth_date, sect):
    if sect == 'Day':
        order = ['Sun', 'Venus', 'Mercury', 'Mars', 'Jupiter', 'Saturn', 'Moon']
    else:
        order = ['Moon', 'Venus', 'Sun', 'Mercury', 'Mars', 'Jupiter', 'Saturn']
    
    # 현재 나이에 따라 활성화된 주기 계산
    ...
```

**언제 구현?**: 장기 운세 분석이 필요할 때

---

### 2. Zodiacal Releasing (황도 해방)

**목적**: 정밀한 타이밍 분석 (Peak 시기 파악)

**원리**:
- Lot of Fortune/Spirit에서 출발
- 각 사인별로 정해진 연도만큼 지배
- Level 1 (대주기) + Level 2 (세부 주기) 구조

**사인별 지배 연도**:
```python
SIGN_YEARS = {
    'Aries': 15, 'Taurus': 8, 'Gemini': 20, 'Cancer': 25,
    'Leo': 19, 'Virgo': 20, 'Libra': 8, 'Scorpio': 15,
    'Sagittarius': 12, 'Capricorn': 27, 'Aquarius': 30, 'Pisces': 12
}
```

**구현 난이도**: 🔴 높음 (Level 2까지 구현 시 복잡)

**언제 구현?**: 고급 사용자 대상 / 정밀 타이밍 필요 시

---

### 3. Transits (현재 행성 영향)

**목적**: 현재 행성 위치가 네이탈 차트에 미치는 영향

**원리**:
- 현재 행성 위치 계산 (Swiss Ephemeris API)
- 네이탈 차트와 비교하여 Aspect 형성 확인
- Annual Profections의 Lord와의 관계 분석

**구현 난이도**: 🟡 중간

**구현 방법**:
```python
def calculate_transits(natal_planets, current_date):
    # 1. 현재 행성 위치 계산 (Swiss Ephemeris)
    current_planets = calculate_planets_for_date(current_date)
    
    # 2. 네이탈 행성과 비교
    transiting_aspects = []
    for transit_p in current_planets:
        for natal_p in natal_planets:
            aspect = check_aspect(transit_p['position'], natal_p['position'])
            if aspect:
                transiting_aspects.append({
                    'transit': transit_p['name'],
                    'natal': natal_p['name'],
                    'aspect': aspect
                })
    
    return transiting_aspects
```

**언제 구현?**: 실시간 운세 분석이 필요할 때

---

## 구현 우선순위 권장

1. **현재**: Annual Profections로 충분 (연간 테마)
2. **다음**: Transits (실시간 분석 추가 시)
3. **나중**: Decennials (장기 운세 추가 시)
4. **선택**: Zodiacal Releasing (고급 기능)

---

## 참고 자료

- Vettius Valens, *Anthologies* (2세기)
- Chris Brennan, *Hellenistic Astrology* (2017)
- The Astrology Podcast - Zodiacal Releasing episodes
