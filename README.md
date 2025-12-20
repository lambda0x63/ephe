# 고전 천궁도 분석기 (Classical Natal Chart)

헬레니즘 점성술 전통을 현대 웹 기술로 구현한 정밀 천궁도 계산 및 분석 서비스.

## 1. 프로젝트 개요

* **목표**: 고전 점성술(Hellenistic Astrology) 원리에 충실한 정밀 차트 시각화 및 분석 도구 개발.
* **특징**: 상업적 디자인을 배제한 '고전 기구(Classical Instrument)' 스타일의 디자인 언어 채택.
* **타겟**: 정통 점성술 연구자 및 고전적인 미학을 선호하는 사용자.

## 2. 주요 기능

* **독자적 차트 엔진**: 외부 라이브러리 없이 직접 구현한 Vanilla JS 기반 SVG 벡터 렌더링 엔진.
  * 1도 단위 정밀 눈금(Tick Marks) 및 12 별자리/행성 기호의 벡터 시각화.
  * Whole Sign House 시스템 기반의 하우스 분할 및 번호 표기.
  * Text-Only 심볼(VS-15) 사용으로 이모지 변환 방지 및 디자인 통일성 확보.
* **정밀 천문 계산**: Swiss Ephemeris (`swisseph`) C-Extension을 통한 고속/고정밀 천체 위치 연산.
  * 7행성 및 주요 감응점(ASC, MC, Nodes, Chiron) 위치 계산.
  * 5대 주요 애스펙트(합, 충, 삼각, 사각, 육각) 및 허용 오차(Orb) 적용.
* **사용자 경험 (UX)**:
  * **현지화**: `Noto Serif KR` 폰트 적용 및 전문 점성 용어 한국어화 완료.
  * **히스토리 관리**: 분석된 차트의 비동기 저장, 조회, 삭제 기능 (HTMX 기반).
  * **반응형 UI**: 데스크탑 및 모바일 환경에 최적화된 종이 질감(Paper Texture) 인터페이스.

## 3. 기술 스택 (Tech Stack)

### Backend

* **FastAPI**: 고성능 비동기 Python 웹 프레임워크.
* **Jinja2**: 서버 사이드 렌더링(SSR) 및 템플릿 엔진.
* **SQLAlchemy + SQLite**: 경량화된 ORM 및 데이터베이스 관리.
* **Pydantic**: 엄격한 데이터 유효성 검사 및 타입 관리.

### Frontend

* **HTMX**: HTML 속성(Attributes)을 활용한 AJAX 요청 및 DOM 부분 업데이트 (SPA급 사용자 경험 제공).
* **Alpine.js**: 경량화된 반응형 상태 관리 및 UI 인터랙션 처리 (Input Drawer, Tab 등).
* **Vanilla JavaScript**: SVG DOM 조작을 통한 고성능 차트 렌더링 (ChartEngine 클래스).
* **CSS Variables**: 테마 색상 및 폰트의 중앙 집중식 관리.

## 4. 설치 및 실행 가이드

### 필수 요건

* Python 3.10 이상

### 설치 절차

1. 가상환경 생성 및 활성화:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Mac/Linux
    ```

2. 의존성 패키지 설치:

    ```bash
    pip install -r requirements.txt
    ```

### 서버 실행

개발 모드(Hot Reload)로 서버 시작:

```bash
python3 -m uvicorn app.main:app --reload
```

* 접속 주소: `http://localhost:8000`

## 5. 프로젝트 구조

```
.
├── app/
│   ├── main.py            # 애플리케이션 진입점 및 설정
│   ├── dependencies.py    # 공통 의존성 (DB 세션, 템플릿 등)
│   ├── database.py        # DB 연결 및 모델 정의
│   ├── routers/           # URL 라우팅 핸들러 (HTMX, Pages, API)
│   ├── services/          # 핵심 비즈니스 로직 (차트 계산, 천문 연산)
│   ├── templates/         # HTML 템플릿 (Jinja2)
│   └── utils/             # 지오코딩, 시간대 변환 등 유틸리티
├── public/                # 정적 파일 (CSS, JS 엔진, 이미지)
├── requirements.txt       # 패키지 의존성 목록
└── README.md              # 프로젝트 문서
```
