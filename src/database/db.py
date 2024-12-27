from pymongo import MongoClient
from config import DB_URI

client = MongoClient(DB_URI)
db = client.chess_review_app

def get_db():
    return db