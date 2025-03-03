from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    # origins = [
    #     "http://localhost:3000",  # 允许本地前端开发环境
    #     "https://yourfrontenddomain.com",  # 允许生产环境中的前端
    # ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许的来源列表
        allow_credentials=True,  # 允许发送 cookies
        allow_methods=["*"],     # 允许所有 HTTP 方法
        allow_headers=["*"],     # 允许所有的请求头
    )
