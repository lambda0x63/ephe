#!/bin/bash

# 프로젝트 디렉토리 설정
PROJECT_DIR="/var/www/natal-fastapi"

echo ">>> 배포 프로세스 시작: $PROJECT_DIR"

# 1. 디렉토리 이동
if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR"
else
    echo "에러: $PROJECT_DIR 디렉토리가 존재하지 않습니다."
    exit 1
fi

# 2. 최신 코드 가져오기
echo ">>> Git Pull..."
git pull origin main

# 3. 가상환경 활성화 (필요한 경우) 및 의존성 설치
# FastAPI/Python 환경이라고 가정합니다.
if [ -d "venv" ]; then
    source venv/bin/activate
    echo ">>> 의존성 업데이트 (pip)..."
    pip install -r requirements.txt
fi

# 4. PM2를 통한 프로세스 재시작
# ecosystem.config.js 파일을 사용하여 무중단 재시작(reload)을 수행합니다.
echo ">>> PM2 Reload..."
pm2 reload ecosystem.config.js

echo ">>> 배포가 완료되었습니다!"
pm2 status
