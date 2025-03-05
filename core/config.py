import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# 加载 .env 文件
load_dotenv()

class Configs(BaseSettings):
    MONGODB_NAME: str = os.getenv("MONGODB_NAME")
    MONGODB_URL: str  = os.getenv("MONGODB_URL")
    class Config:
        env_file = ".env"
        extra = 'allow'

config = Configs()