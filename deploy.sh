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

# 2. 로컬 변경사항 초기화 및 최신 코드 가져오기
echo ">>> Git Reset & Pull..."
git reset --hard HEAD
git clean -fd
BRANCH=$(git branch --show-current)
if [ -z "$BRANCH" ]; then BRANCH="main"; fi
git pull origin $BRANCH || git pull origin master

# 3. 의존성 설치 (전역 python3 사용)
echo ">>> 의존성 설치 (전역)..."
python3 -m pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt
fi
python3 -m pip install uvicorn

# 3.5 Cache Busting (JS 버전 자동 갱신)
echo ">>> Cache Busting: chart_engine.js..."
TIMESTAMP=$(date +%s)
# Linux(Ubuntu/CentOS) 기준 sed 문법
sed -i "s/chart_engine.js?v=[^\"]*/chart_engine.js?v=$TIMESTAMP/g" app/templates/dashboard.html

# 4. PM2를 통한 프로세스 재시작
echo ">>> PM2 Reload..."
# ecosystem.config.js가 절대경로를 가리키도록 설정되어 있어야 함
pm2 reload ecosystem.config.js || pm2 start ecosystem.config.js

echo ">>> 배포가 완료되었습니다!"
pm2 status

