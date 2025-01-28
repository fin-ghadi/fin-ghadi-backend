from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import User, Activity, UserActivity, Location , Quote

MONGO_URI = "mongodb://localhost:27017/fin-ghadi"


async def connect_to_mongo():
    client = AsyncIOMotorClient(MONGO_URI)
    database = client.get_database()
    await init_beanie(database, document_models=[User, Activity, UserActivity, Location, Quote])
 