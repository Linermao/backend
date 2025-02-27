import os
from public.usage import USAGE as html
from api.hello import router as hello_router
from api.random import router as random_router
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
# GitHub 仓库的相关信息
LOCAL_HOST = os.getenv("LOCAL_HOST", "http://localhost:3000")
VERCEL_HOST = os.getenv("VERCEL_HOST")

origins = [
    LOCAL_HOST,  # From Nextjs
    VERCEL_HOST,  # Online
]

"""
local test
curl -H "Origin: https://frontend-linermaos-projects.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS https://backend-eta-tan.vercel.app/hello
"""

# 启用 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的域名列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

app.include_router(hello_router, prefix="/hello")
app.include_router(random_router, prefix="/random")


@app.get("/")
def _root():
    return Response(content=html, media_type="text/html")