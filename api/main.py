from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # 允许来自 Vite 开发服务器的请求
    # "https://yourfrontend.com",  # 如果你部署到线上，可以添加你的网站
]

# 启用 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的域名列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

@app.get("/api")
def read_root():
    return {"Hello": "World"}