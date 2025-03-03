import motor.motor_asyncio
from core.config import DATABASE_URL

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client.get_database("MediaArchive")
articles_collection = db.get_collection("articles")
