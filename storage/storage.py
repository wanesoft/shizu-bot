from os import getenv
import motor.motor_asyncio
from aiogram.fsm.storage.mongo import MongoStorage


MONGO_USER = getenv("MONGO_USER")
MONGO_PASS = getenv("MONGO_PASS")
MONGODB_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@127.0.0.1:27017/"


class Storage:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        self.storage = MongoStorage(self.client)