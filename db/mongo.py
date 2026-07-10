from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient("mongodb://root:secretpassword@localhost:27017")
db = client["shop"]
products_collection = db["products"]