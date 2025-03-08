import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# 加载 .env 文件
load_dotenv()

class Configs(BaseSettings):
    # 数据库配置
    MONGODB_NAME: str = os.getenv("MONGODB_NAME")
    MONGODB_URL: str  = os.getenv("MONGODB_URL")

    # JWT 配置
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        extra = 'allow'

config = Configs()