from fastapi import FastAPI
from api.v1.articles import router as articles_router
import uvicorn
# from api.v1.posts import router as posts_router
from core.cors import add_cors_middleware

app = FastAPI()

add_cors_middleware(app)

# 路由注册
app.include_router(articles_router, prefix="/api/v1", tags=["articles"])
# app.include_router(posts_router, prefix="/posts", tags=["posts"])

if __name__ == '__main__':
  uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)