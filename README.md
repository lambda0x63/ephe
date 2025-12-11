# Natal Chart API

고전점성술 기반 네이탈차트 계산 API 서버

## Quick Start

```bash
# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

## API 테스트

```bash
curl -X POST http://localhost:8000/api/v1/natal-chart \
  -H "Content-Type: application/json" \
  -d '{"birth_date": "1999-01-10", "birth_time": "00:31:00", "place_name": "Seoul, South Korea"}'
```

## 문서

- API 문서: http://localhost:8000/docs
- 아키텍처: [docs/architecture.md](docs/architecture.md)
