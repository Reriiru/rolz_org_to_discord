from pymongo import MongoClient
from settings import MONGO_STRING

client = MongoClient(MONGO_STRING)
db = client.rolz_database
