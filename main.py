import uvicorn 
from fastapi import FastAPI
from api.v1.articles import router as articles_router
from contextlib import asynccontextmanager
# from api.v1.posts import router as posts_router
from core.cors import add_cors_middleware
from core.database import init_db, close_db, Database
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """生命周期管理器"""
    # 启动阶段
    try:
        logger.info("Initializing database connection...")
        await init_db()
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

    yield  # 应用运行期

    # 关闭阶段
    try:
        logger.info("Closing database connection...")
        await close_db()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Database shutdown failed: {str(e)}")

app = FastAPI(
    lifespan=lifespan,
    title='My full stack app',
    version='1.0.0'
)

add_cors_middleware(app)

# 路由注册
app.include_router(articles_router, prefix="/api/v1", tags=["articles"])
# app.include_router(posts_router, prefix="/posts", tags=["posts"])

@app.get("/")
async def root():
    if Database.db is None:
        await Database.connect_db()
    return {"status": "ready"}

if __name__ == '__main__':
  uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)