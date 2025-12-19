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

# 2. 최신 코드 가져오기 (브랜치 자동 감지)
echo ">>> Git Pull..."
BRANCH=$(git branch --show-current)
if [ -z "$BRANCH" ]; then BRANCH="main"; fi
git pull origin $BRANCH || git pull origin master

# 3. 가상환경 설정 및 의존성 설치
if [ ! -d "venv" ]; then
    echo ">>> 가상환경 생성 중 (venv)..."
    python3 -m venv venv
fi

echo ">>> 가상환경 활성화 및 의존성 설치..."
source venv/bin/activate
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi
pip install uvicorn  # uvicorn이 확실히 설치되도록 추가

# 4. PM2를 통한 프로세스 재시작
echo ">>> PM2 Reload..."
# ecosystem.config.js가 절대경로를 가리키도록 설정되어 있어야 함
pm2 reload ecosystem.config.js || pm2 start ecosystem.config.js

echo ">>> 배포가 완료되었습니다!"
pm2 status

