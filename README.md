# EPHE (Astrology Practice Tool)

개인 점성술 판독 숙달 및 데이터 아카이빙을 위한 도구임. 고전 점성학 원칙에 충실한 차트 생성과 에스펙트 분석 기능 제공에 집중함.

## 설계 목표
* **시각적 절제**: 흑백 행성 기호 적용을 통해 시각적 힌트를 배제한 직관적 판독 훈련 유도.
* **데이터 정확성**: 모리누스(Morinus) 식 도식 및 1도 단위 정밀 눈금 시스템 적용.
* **기능적 단순화**: 불필요한 장식 요소를 배제하고 점성학적 기하 구조 파악에 최적화함.

## 주요 기능
* **고전 점성학 연산**: 7개 전통 행성, 에센셜 디그니티(Terms, Faces), 섹트 기반 가상점(Lots) 좌표 산출.
* **인터랙티브 에스펙트**: 행성 클릭 시 고전적 발광 반경(Moiety)을 반영한 정밀 각도선 출력.
* **차트 기록 관리**: 생성된 차트 데이터의 자동 저장 및 로컬 데이터베이스 연동 관리.
* **하우스 시스템**: Whole Sign 및 Porphyry 시스템 간 동적 전환 지원.

## 기술 스택
* FastAPI, HTMX, Vanilla CSS
* pyswisseph (Swiss Ephemeris)
* SQLite (SQLAlchemy)

## 설치 및 실행
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---
개인적 점성술 연구 및 숙달을 목적으로 개발된 도구임.
