from pymongo import MongoClient
from settings import MONGO_URL

client = MongoClient(MONGO_URL)
db = client.rolz_database
