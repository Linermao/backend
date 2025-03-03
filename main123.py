import os
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from random import choice
from bson import ObjectId

load_dotenv()

api_router = APIRouter()

app = FastAPI()

LOCAL_HOST = os.getenv("LOCAL_HOST", "http://localhost:3000")
VERCEL_HOST = os.getenv("VERCEL_HOST")
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = "MediaArchive"
COLLECTION_NAME = "posts"

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

def objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

# 异步创建 MongoDB 客户端
client: AsyncIOMotorClient = None
db = None
collection = None

@app.on_event("startup")
async def startup_db():
    global client
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGODB_URL)

@app.on_event("shutdown")
async def shutdown_db():
    global client
    print("Closing MongoDB connection...")
    if client:
        client.close()

@app.get("/posts")
async def get_posts():
    global db, collection
    db = client.get_database(DATABASE_NAME)
    collection = db.get_collection(COLLECTION_NAME)

    posts_cursor = collection.find()
    posts = await posts_cursor.to_list(length=None)

    for post in posts:
        post['_id'] = objectid_to_str(post['_id'])
        
    return posts

@app.get("/")
def _root():
    return Response(content="<html><body><h1>FastAPI App</h1></body></html>", media_type="text/html")
