# Ephe

헬레니즘 점성술 기반의 네이탈 차트 분석 서비스

## 🛠️ 기술 스택

| 역할 | 기술 |
|------|-----|
| Backend | **FastAPI** + Jinja2 (SSR) |
| Interaction | **HTMX** (JS 없이 AJAX 처리) |
| State | **Alpine.js** (가벼운 UI 상태 관리) |
| Visualization | **Vanilla JS** (SVG 차트 엔진) |
| DB | **PostgreSQL** |

## 🧠 설계 원칙

1. **서버 주도 UI** - 서버가 HTML을 렌더링하고, 클라이언트는 뷰어 역할만 수행
2. **Zero-Build** - 번들러 없음. 수정 후 새로고침하면 즉시 반영
3. **행동의 지역성** - `hx-post`, `hx-target` 등 HTML 속성만으로 동작 파악 가능

## 📁 구조

```text
app/
├── services/     # 천문 계산 로직 (Swiss Ephemeris)
├── routers/      # HTMX 부분 렌더링 / 전체 페이지 분리
├── templates/    # Jinja2 템플릿
public/
└── js/chart_engine.js  # SVG 차트 렌더링 엔진
```

## 🚀 실행

```bash
# 개발
python3 -m uvicorn app.main:app --reload --port 8000

# 배포
./deploy.sh
```
