from pydantic import BaseModel
from typing import List
from datetime import datetime

class Article(BaseModel):
    name: str
    title: str
    cover_img: str
    date: datetime
    modify_date: datetime
    tags: List[str]
    category: str
    content: str
    status: str
    views: int
