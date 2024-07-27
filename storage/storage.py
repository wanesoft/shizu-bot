import json
import motor.motor_asyncio

from os import getenv
from aiogram.fsm.storage.mongo import MongoStorage

from storage.entities import *


MONGO_USER = getenv("MONGO_USER")
MONGO_PASS = getenv("MONGO_PASS")
MONGODB_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@127.0.0.1:27017/"
AIOGRAM_DB = "aiogram_fsm"
REFS_COLLECTION = "refs"
USERS_COLLECTION = "users"
DATA_COLLECTIONS = "data"


class Storage:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        self.storage = MongoStorage(self.client)
        # @todo: before start create `REFS_COLLECTION` collection
        # self.client.get_database(AIOGRAM_DB).create_collection(REFS_COLLECTION)

    async def get_refinfo_by_ref_id(self, ref_id) -> RefInfo:
        db = self.client.get_database(AIOGRAM_DB)
        collection = db.get_collection(REFS_COLLECTION)
        result = await collection.find_one(ref_id)
        if not result:
            return None
        model = json.loads(result[DATA_COLLECTIONS])
        return RefInfo.model_validate(model)
    
    async def create_refinfo_by_ref_id(self, ref_id, user_id):
        db = self.client.get_database(AIOGRAM_DB)
        collection = db.get_collection(REFS_COLLECTION)
        ref_info = RefInfo.create(user_id)
        await collection.insert_one({"_id": ref_id, DATA_COLLECTIONS: json.dumps(ref_info.__dict__)})
    
    async def update_refinfo_by_ref_id(self, ref_id, ref_info: RefInfo):
        db = self.client.get_database(AIOGRAM_DB)
        collection = db.get_collection(REFS_COLLECTION)
        filter = {"_id": ref_id}
        update = {'$set': {DATA_COLLECTIONS: json.dumps(ref_info.__dict__)}}
        await collection.update_one(filter, update)
    
    async def get_user_by_id(self, user_id) -> User:
        db = self.client.get_database(AIOGRAM_DB)
        collection = db.get_collection(USERS_COLLECTION)
        db_id = User.generate_db_id(user_id)
        result = await collection.find_one(db_id)
        if not result:
            return None
        model = json.loads(result[DATA_COLLECTIONS])
        return User.model_validate(model)

    async def create_user(self, user: User):
        db = self.client.get_database(AIOGRAM_DB)
        collection = db.get_collection(USERS_COLLECTION)
        await collection.insert_one({"_id": user.db_id, DATA_COLLECTIONS: json.dumps(user.__dict__)})
    
    async def update_user(self, user: User):
        db = self.client.get_database(AIOGRAM_DB)
        collection = db.get_collection(USERS_COLLECTION)
        filter = {"_id": user.db_id}
        update = {'$set': {DATA_COLLECTIONS: json.dumps(user.__dict__)}}
        await collection.update_one(filter, update)


s = Storage()