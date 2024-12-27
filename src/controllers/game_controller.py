from database.gamedatabase import save_game_to_db, get_all_games as db_get_all_games, get_game_by_id as db_get_game_by_id

def save_game(pgn, analysis):
    inserted_id = save_game_to_db(pgn, analysis)
    print(f"Game saved with ID: {inserted_id}")
    return inserted_id
    #save_game_to_db(pgn, analysis)

def get_games():
    return db_get_all_games()

def get_game_by_id(game_id):
    return db_get_game_by_id(game_id)