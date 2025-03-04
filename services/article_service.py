import base64
from core.database import articles_collection
from pymongo.errors import PyMongoError
from services.handle_error import ErrorHandler

async def get_article(title: str) -> dict:
    try:
        article = await articles_collection.find_one({"title": str(title)})
        
        if not article:
            ErrorHandler.handle_not_found_error()

        article["_id"] = str(article["_id"])

        if isinstance(article.get("content"), (str, bytes)):  # 确保content字段是有效的
            try:
                article["content"] = base64.b64decode(article["content"]).decode('utf-8')
            except base64.binascii.Error:
                ErrorHandler.handle_base64_error()
        else:
            ErrorHandler.handle_invalid_content_error()
        
        return article
    except PyMongoError as e:
        ErrorHandler.handle_mongodb_error(e)
    except Exception as e:
        ErrorHandler.handle_unexpected_error(e)


async def get_all_articles(start: int = 0, limit: int = 100) -> list:
    try:
        articles = []
        cursor = articles_collection.find().skip(start).limit(limit)
        async for article in cursor:
            article["_id"] = str(article["_id"])
            articles.append(article)
        return articles
    except PyMongoError as e:
        ErrorHandler.handle_mongodb_error(e)
    except Exception as e:
        ErrorHandler.handle_unexpected_error(e)


async def get_articles_num() -> dict:
    try:
        num = await articles_collection.count_documents({})
        return {"articles_num": num}
    except PyMongoError as e:
        ErrorHandler.handle_mongodb_error(e)
    except Exception as e:
        ErrorHandler.handle_unexpected_error(e)