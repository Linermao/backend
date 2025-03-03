from bson import ObjectId
from fastapi import HTTPException

from models.article import Article
from core.database import articles_collection

async def create_article(article: Article):
    article_dict = article.dict()
    result = await articles_collection.insert_one(article_dict)
    return {**article_dict, "_id": str(result.inserted_id)}

async def get_article(article_id: str):
    article = await articles_collection.find_one({"_id": ObjectId(article_id)})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article["_id"] = str(article["_id"])
    return article

async def get_all_articles(limit=100):
    articles = []
    cursor = articles_collection.find().limit(limit)
    async for article in cursor:
        article["_id"] = str(article["_id"])
        articles.append(article)
    return articles