# Natal Chart API - Architecture

## 목적
고전점성술 기반 네이탈차트 계산 API 서버

- 입력: 생년월일시 + 출생지(도시명 또는 좌표)
- 출력: 프론트엔드에서 SVG 차트 렌더링용 데이터

---

## 설계 철학

> **오버엔지니어링 금지. 필요한 것만 만든다.**

### YAGNI (You Aren't Gonna Need It)
- 지금 필요하지 않은 기능은 만들지 않는다
- "나중에 필요할 것 같아서" 미리 만드는 것 금지

### KISS (Keep It Simple, Stupid)
- 복잡한 추상화보다 단순한 구현 우선
- 서비스 레이어 최소화

### DRY (Don't Repeat Yourself)
- 반복되는 코드만 추상화
- 2번 이상 반복될 때만 함수로 분리

---

## 기술 스택

- **FastAPI** - API 서버
- **pyswisseph** - 천체력 계산 (Swiss Ephemeris)
- **geopy** - 도시명 → 좌표 변환 (Geocoding)
- **timezonefinder** - 좌표 → 타임존 자동 추론

---

## 고전점성술 규칙

### 7개 천체
| 천체 | 영문 | 지배 사인 |
|------|------|-----------|
| ☉ 태양 | Sun | Leo |
| ☽ 달 | Moon | Cancer |
| ☿ 수성 | Mercury | Gemini, Virgo |
| ♀ 금성 | Venus | Taurus, Libra |
| ♂ 화성 | Mars | Aries, Scorpio |
| ♃ 목성 | Jupiter | Sagittarius, Pisces |
| ♄ 토성 | Saturn | Capricorn, Aquarius |

> ❌ 외행성(천왕성, 해왕성, 명왕성) 사용 안함

### 하우스 시스템
**Whole Sign** 방식만 사용
- ASC가 위치한 사인 전체 = 1하우스
- 각 하우스 = 정확히 1개 사인(30°)

### 애스펙트 (5개)
| 애스펙트 | 각도 | 오브 |
|----------|------|------|
| Conjunction (컨정션) | 0° | ±8° |
| Sextile (섹스타일) | 60° | ±6° |
| Square (스퀘어) | 90° | ±8° |
| Trine (트라인) | 120° | ±8° |
| Opposition (어포지션) | 180° | ±8° |

---

## API

### `POST /api/v1/natal-chart`

**Request:**
```json
{
  "birth_date": "1999-01-10",
  "birth_time": "00:31:00",
  "place_name": "Daegu, South Korea"
}
```

**Response:**
```json
{
  "planets": [
    {
      "name": "Sun",
      "name_ko": "태양",
      "symbol": "☉",
      "sign": "Capricorn",
      "sign_ko": "염소자리",
      "degree": 18.92,
      "degree_formatted": "18°54'",
      "house": 4,
      "retrograde": false,
      "position": 288.92
    }
  ],
  "houses": [
    {
      "number": 1,
      "sign": "Libra",
      "sign_ko": "천칭자리",
      "degree": 0.0
    }
  ],
  "aspects": [
    {
      "planet1": "Sun",
      "planet1_ko": "태양",
      "planet2": "Moon",
      "planet2_ko": "달",
      "type": "Square",
      "type_ko": "스퀘어",
      "angle": 90,
      "orb": 0.52
    }
  ],
  "ascendant": {
    "sign": "Libra",
    "sign_ko": "천칭자리",
    "degree": 16.63,
    "degree_formatted": "16°37'"
  },
  "input": {
    "birth_date": "1999-01-10",
    "birth_time": "00:31:00",
    "latitude": 35.8713,
    "longitude": 128.6018,
    "timezone": "Asia/Seoul"
  }
}
```

### `GET /health`
헬스체크

---

## 프로젝트 구조

```
natal-fastapi/
├── app/
│   ├── main.py           # FastAPI 앱
│   ├── models.py         # Pydantic 모델
│   ├── services/
│   │   ├── chart.py      # 차트 계산 오케스트레이션
│   │   ├── planets.py    # 천체 위치 계산
│   │   ├── houses.py     # Whole Sign 하우스
│   │   └── aspects.py    # 애스펙트 계산
│   └── utils/
│       ├── geocoding.py  # 도시명 → 좌표
│       └── timezone.py   # 좌표 → 타임존
├── docs/
│   └── architecture.md
├── venv/
├── requirements.txt
└── README.md
```

---

## 구현 범위

### ✅ 완료
- 7개 천체 위치 계산
- Whole Sign 하우스
- 5개 애스펙트
- 도시명 Geocoding
- 타임존 자동 추론
- 한국어 지원 (천체, 사인, 애스펙트)
- 도°분' 형식 지원

### ❌ 제외 (나중에)
- Lunar Nodes, Part of Fortune
- 트랜짓, 프로그레션
- 다른 하우스 시스템
