import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 获取环境变量
DATABASE_URL = os.getenv("DATABASE_URL")
# SECRET_KEY = os.getenv("SECRET_KEY")
# DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
# TEST_USERNAME = os.getenv("TEST_USERNAME")
# TEST_PASSWORD = os.getenv("TEST_PASSWORD")

# 如果没有数据库URL，抛出错误
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found in environment variables")