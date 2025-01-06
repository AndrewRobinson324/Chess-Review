import chess.engine
from pymongo import MongoClient

def analyze_game(fen, depth=15, multi_pv=3):
    stockfish_path = "C:/Users/rocky/OneDrive/Documents/Chess Review bot/stockfish/stockfish-windows-x86-64-sse41-popcnt.exe"
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        results = engine.analyse(chess.Board(fen), chess.engine.Limit(depth=depth), multipv=multi_pv)
        print(f"Analysis results for FEN {fen}: {results}")
        return serialize_analysis(results, fen)

def serialize_analysis(results, fen):
    serialized_results = []
    for result in results:
        print(f"Result: {result}")  # Add logging to print the result
        score = result['score'].relative
        cp_score = score.score()
        classification = classify_move(cp_score)
        serialized_result = {
            'score': cp_score,
            'mate': score.mate(),
            'pv': [move.uci() for move in result.get('pv', [])],
            'classification': classification,
            'fen': fen
        }
        print(f"Serialized result: {serialized_result}")  # Add logging to print the serialized result

        # Check if the move is a mistake or blunder and save it to the database
        if classification in ['Mistake', 'Blunder']:
            save_critical_position(fen, classification)
        
        serialized_results.append(serialized_result)
    
    return serialized_results

def classify_move(score_diff_cp):
    if score_diff_cp < 20:
        return 'Best move'
    elif score_diff_cp < 80:
        return 'Good move'
    elif score_diff_cp < 150:
        return 'Mistake'
    else:
        return 'Blunder'

# Initialize the database connection
client = MongoClient('localhost', 27017)
db = client['chess_review']

def save_critical_position(fen, classification):
    # Save the critical position to the database
    db.critical_positions.insert_one({
        'fen': fen,
        'classification': classification
    })