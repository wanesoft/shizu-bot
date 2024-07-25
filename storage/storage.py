import json
import motor.motor_asyncio

from os import getenv
from aiogram.fsm.storage.mongo import MongoStorage
from bson import ObjectId

from storage.entities import *


MONGO_USER = getenv("MONGO_USER")
MONGO_PASS = getenv("MONGO_PASS")
MONGODB_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@127.0.0.1:27017/"
AIOGRAM_DB = "aiogram_fsm"
REFS_COLLECTION = "refs"


class Storage:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        self.storage = MongoStorage(self.client)
        # @todo: before start create `REFS_COLLECTION` collection
        # self.client.get_database(AIOGRAM_DB).create_collection(REFS_COLLECTION)

    async def get_refinfo_by_ref_id(self, ref_id):
        db = self.client.get_database(AIOGRAM_DB)
        collection = db.get_collection(REFS_COLLECTION)
        result = await collection.find_one(ref_id)
        asd = json.loads(result["data"])
        return RefInfo.model_validate(asd)
    
    async def create_refinfo_by_ref_id(self, ref_id, user_id):
        db = self.client.get_database(AIOGRAM_DB)
        collection = db.get_collection(REFS_COLLECTION)
        ref_info = RefInfo.create(user_id)
        await collection.insert_one({"_id": ref_id, "data": json.dumps(ref_info.__dict__)})
    
    async def update_refinfo_by_ref_id(self, ref_id, ref_info: RefInfo):
        db = self.client.get_database(AIOGRAM_DB)
        collection = db.get_collection(REFS_COLLECTION)
        filter = {"_id": ref_id}
        update = {'$set': {"data": json.dumps(ref_info.__dict__)}}
        await collection.update_one(filter, update)


s = Storage()