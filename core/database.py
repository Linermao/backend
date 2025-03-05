from motor.motor_asyncio import AsyncIOMotorClient
from core.config import config
import asyncio

def get_db_client():
    try:
        # 尝试获取当前运行的事件循环
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # 如果没有运行的事件循环，则创建一个新的
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    client = AsyncIOMotorClient(config.MONGODB_URL)
    return client

def get_collection(collection_name: str):
    """ 获取指定的 MongoDB 集合 """
    client = get_db_client() 
    database = client.get_database(config.MONGODB_NAME)  
    collection = database.get_collection(collection_name) 
    return collection