from fastapi import FastAPI, Request, Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

from app.database import engine
from app import models
from app.routers import pages, partials, api
from app.dependencies import templates

# DB 테이블 생성
models.Base.metadata.create_all(bind=engine)

# 비밀번호 설정 (환경변수 또는 기본값)
AUTH_USERNAME = os.getenv("EPHE_USER", "admin")
AUTH_PASSWORD = os.getenv("EPHE_PASS", "q1w2e3r4")
SECRET_KEY = os.getenv("SECRET_KEY", "ephe-secret-key-change-me")


class SessionAuthMiddleware(BaseHTTPMiddleware):
    """세션 기반 인증 미들웨어"""
    
    ALLOWED_PATHS = ["/ephe/", "/ephe/login", "/ephe/static"]
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # 허용된 경로는 통과
        for allowed in self.ALLOWED_PATHS:
            if path.startswith(allowed) or path == "/ephe":
                return await call_next(request)
        
        # 세션 확인
        if request.session.get("authenticated"):
            return await call_next(request)
        
        # 인증 안 됨 -> 로그인 페이지로
        return RedirectResponse(url="/ephe/", status_code=303)


app = FastAPI(
    title="Ephe",
    description="Advanced Astrology Calculation Service with HTMX Dashboard",
    version="2.0.0",
    root_path="/ephe"
)

# 인증 미들웨어 (먼저 추가 = 안쪽에서 실행)
app.add_middleware(SessionAuthMiddleware)

# 세션 미들웨어 (나중에 추가 = 바깥쪽에서 먼저 실행되어 세션 설정)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory="public"), name="static")


# 로그인 페이지 (랜딩 페이지 대체)
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("authenticated"):
        return RedirectResponse(url="/ephe/dashboard", status_code=303)
    
    error = request.query_params.get("error", "")
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": error
    })


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == AUTH_USERNAME and password == AUTH_PASSWORD:
        request.session["authenticated"] = True
        return RedirectResponse(url="/ephe/dashboard", status_code=303)
    
    return RedirectResponse(url="/ephe/?error=invalid", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/ephe/", status_code=303)


# 라우터 등록
app.include_router(pages.router)
app.include_router(partials.router)
app.include_router(api.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
