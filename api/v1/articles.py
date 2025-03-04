from fastapi import APIRouter
from services.article_service import get_article, get_all_articles, get_articles_num

router = APIRouter()

# @router.post("/api/v1/article")
# async def create_article_endpoint(article: Article):
#     return await create_article(article)

@router.get("/articles")
async def get_all_articles_endpoint(start: int = 0, limit: int = 0):
    return await get_all_articles(start, limit)

@router.get("/articles/num")
async def get_articles_num_endpoint():
    return await get_articles_num()

@router.get("/articles/{article_title}")
async def get_article_endpoint(article_title: str):
    return await get_article(article_title)
