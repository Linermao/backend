from fastapi import APIRouter
from models.article import Article
from services.article_service import create_article, get_article, get_all_articles

router = APIRouter()

# @router.post("/api/v1/article")
# async def create_article_endpoint(article: Article):
#     return await create_article(article)

@router.get("/articles")
async def get_article_endpoint(article_id: str = None):
    if article_id:
        # 如果带有 article_id 参数，获取特定文章
        return await get_article(article_id)
    else:
        # 如果没有带 article_id 参数，返回所有文章
        return await get_all_articles()

