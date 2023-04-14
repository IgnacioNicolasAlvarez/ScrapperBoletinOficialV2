import pymongo

from src.model.model import Aviso


class MongoRepository:
    def __init__(self, user, password, server, db, collection):
        self.user = user
        self.password = password
        self.server = server
        self.db = db
        self.collection = collection
    
    def insert_one(self, aviso: Aviso):
        client = pymongo.MongoClient(
            f"mongodb+srv://{self.user}:{self.password}@{self.server}/?retryWrites=true&w=majority"
        )
        db = client[self.db]
        collection = db[self.collection]
        collection.insert_one(aviso.dict())