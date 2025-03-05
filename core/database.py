from motor.motor_asyncio import AsyncIOMotorClient
from core.config import config
from typing import Optional
import logging

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorClient] = None

    @classmethod
    async def connect_db(cls):
        """建立数据库连接"""
        try:
            if config.MONGODB_URL is None:
                raise ValueError("MongoDB URL not configured")

            cls.client = AsyncIOMotorClient(
                config.MONGODB_URL,
                maxPoolSize=100,  # 适合serverless的最大连接池大小
                minPoolSize=10,
                connectTimeoutMS=5000,
                serverSelectionTimeoutMS=5000
            )
            cls.db = cls.client[config.MONGODB_NAME]
            
            # 测试连接
            await cls.client.server_info()
            logging.info("Successfully connected to MongoDB")
            
            return cls.db
            
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    @classmethod
    async def close_db(cls):
        """关闭数据库连接"""
        if cls.client:
            cls.client.close()
            logging.info("MongoDB connection closed")
            
    @classmethod
    def get_collection(cls, collection_name: str):
        """获取集合实例"""
        if cls.db is None:
            raise RuntimeError("Database not initialized")
        return cls.db[collection_name]

# 初始化数据库连接（在FastAPI生命周期中使用）
async def init_db():
    await Database.connect_db()

# 关闭数据库连接（在FastAPI生命周期中使用）
async def close_db():
    await Database.close_db()