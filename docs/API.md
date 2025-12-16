# Natal Chart API Documentation (v1)

## Base URL
`http://localhost:8000` (Local)

---

## 1. 헬스 체크 (Health Check)
서버 상태를 확인합니다.

- **Endpoint**: `GET /health`
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

---

## 2. 도시 검색 (Search Place)
도시 이름으로 좌표를 검색합니다. (Autocomplete 기능)

- **Endpoint**: `GET /api/v1/search-place`
- **Parameters**:
  - `query` (string, required): 검색할 도시 이름 (예: "Seoul", "대구")

- **Response**:
  ```json
  {
    "results": [
      {
        "name": "Daegu, South Korea",
        "display_name": "Daegu",
        "latitude": 35.87139,
        "longitude": 128.601763
      },
      ...
    ]
  }
  ```

---

## 3. 네이탈 차트 생성 (Calculate Natal Chart)
출생 정보를 바탕으로 서양 고전 점성술(Whole Sign House) 차트를 계산하고, AI 간명용 요약 텍스트를 생성합니다.

- **Endpoint**: `POST /api/v1/natal-chart`
- **Content-Type**: `application/json`

- **Request Body**:
  ```json
  {
    "birth_date": "1999-01-10",
    "birth_time": "14:30:00",
    "place_name": "Seoul" 
    // 또는 latitude, longitude 직접 입력 가능
    // "latitude": 37.5665,
    // "longitude": 126.9780
  }
  ```

- **Response**:
  - **planets**: 7행성 위치 (황도 경도, 하우스, 역행 여부)
  - **houses**: 1~12하우스 정보 (Whole Sign 시스템)
  - **aspects**: 행성 간 각도 (Major Aspects: 0, 60, 90, 120, 180)
  - **ascendant**: 상승궁 (ASC) 정보
  - **midheaven**: 중천 (MC) 정보
  - **fortuna**: 포르투나 (Part of Fortune)
  - **summary_prompt**: **(New)** AI에게 입력하기 최적화된 구조화된 차트 리포트 텍스트

- **Response Example**:
  ```json
  {
    "planets": [...],
    "houses": [...],
    "aspects": [...],
    "ascendant": {
      "sign": "Libra",
      "sign_ko": "천칭자리",
      "degree_formatted": "16°37'"
    },
    "summary_prompt": "=== 🏛️ 고전 점성술(Hellenistic) 차트 분석 데이터 ===\n\n[1] 핵심 지표...\n..."
  }
  ```
