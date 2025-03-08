from pydantic import BaseModel
from typing import List
from datetime import datetime

class Article(BaseModel):
    title: str
    content: str

