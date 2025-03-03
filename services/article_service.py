from bson import ObjectId
from fastapi import HTTPException

from models.article import Article
from core.database import articles_collection

import base64

async def create_article(article: Article):
    article_dict = article.dict()
    result = await articles_collection.insert_one(article_dict)
    return {**article_dict, "_id": str(result.inserted_id)}

# async def get_article(article_id: str):
#     article = await articles_collection.find_one({"_id": ObjectId(article_id)})
#     if not article:
#         raise HTTPException(status_code=404, detail="Article not found")
#     article["_id"] = str(article["_id"])
#     return article

import base64
from fastapi import HTTPException
from pymongo.errors import PyMongoError

async def get_article(title: str):
    try:
        # 查询文章
        article = await articles_collection.find_one({"title": str(title)})
        
        # 如果找不到文章
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # 解码内容
        article["_id"] = str(article["_id"])
        
        try:
            # 尝试解码内容
            article["content"] = base64.b64decode(article["content"]).decode('utf-8')
        except base64.binascii.Error as e:
            # 如果 Base64 解码失败，返回错误
            raise HTTPException(status_code=400, detail="Base64 decoding error: Invalid encoding")
        
        return article
    except PyMongoError as e:
        # 捕获 MongoDB 的错误
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        # 捕获其他未知错误
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


async def get_all_articles(start=0, limit=0):
    articles = []
    cursor = articles_collection.find().skip(start).limit(limit)
    async for article in cursor:
        article["_id"] = str(article["_id"])
        articles.append(article)
    return articles

async def get_articles_num():
    num = await articles_collection.count_documents({})
    return {"articles_num": num}