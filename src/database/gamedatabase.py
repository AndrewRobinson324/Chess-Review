from pymongo import MongoClient
from config import DB_URI
import datetime
from analysis.stockfish import serialize_analysis
from bson.objectid import ObjectId
from config import DB_URI

client = MongoClient(DB_URI)
db = client.chess_review_app

def save_game_to_db(pgn, analysis):
    game = {
        "pgn": pgn,
        "analysis": [serialize_analysis(a) for a in analysis],
        "date": datetime.datetime.utcnow()
    }
    result = db.games.insert_one(game)
    inserted_id = result.inserted_id
    print(f"Game saved with ID: {inserted_id}")
    return inserted_id

def get_all_games():
    games = list(db.games.find())
    for game in games:
        game['_id'] = str(game['_id']) # convert OBjectID to String
    return games

def get_game_by_id(game_id):
    game = db.games.find_one({"_id": ObjectId(game_id)})
    if game:
        game['_id'] = str(game['_id'])
    return game