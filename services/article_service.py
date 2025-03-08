from models.article import Article
from urllib.parse import unquote
from core.database import get_collection
from pymongo.errors import PyMongoError
from utils.handle_error import ErrorHandler
from core.config import config

from utils.base64tool import encode_base64, decode_base64

database_name = 'MediaArchive'
collection_name = 'articles'

async def get_article(title: str) -> dict:
    try:
        # 解码路径
        decoded_name = unquote(title)
        collection = get_collection(database_name, collection_name)
        article = await collection.find_one({"title": decoded_name})

        if not article:
            ErrorHandler.handle_not_found_error(f"article: {title}")

        article["_id"] = str(article["_id"])

        if isinstance(article.get("content"), (str, bytes)):  # 确保content字段是有效的
            article["content"] = encode_base64(article["content"])
        else:
            ErrorHandler.handle_invalid_content_error()
        
        return article
    except PyMongoError as e:
        ErrorHandler.handle_mongodb_error(e)
    except Exception as e:
        ErrorHandler.handle_unexpected_error(e)

async def get_all_articles(start: int = 0, limit: int = 100) -> list:
    try:
        collection = get_collection(database_name, collection_name)
        articles = []
        cursor = collection.find().skip(start).limit(limit)
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
        collection = get_collection(database_name, collection_name)
        num = await collection.count_documents({})
        return {"articles_num": num}
    except PyMongoError as e:
        ErrorHandler.handle_mongodb_error(e)
    except Exception as e:
        ErrorHandler.handle_unexpected_error(e)

async def post_article(article: Article):
    try:
        collection = get_collection(database_name, collection_name)
        encoded_content = encode_base64(article.content)

        result = collection.insert_one({
            "title": article.title,
            "content": encoded_content
        })

        return {"message": "Article created successfully", "title": article.title}
    except PyMongoError as e:
        ErrorHandler.handle_mongodb_error(e)
    except Exception as e:
        ErrorHandler.handle_unexpected_error(e)
