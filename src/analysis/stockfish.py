import chess.engine

def analyze_game(fen,depth = 15):
    
    stockfish_path = "C:/Users/rocky/OneDrive/Documents/Chess Review bot/stockfish/stockfish-windows-x86-64-sse41-popcnt.exe"

    
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        result = engine.analyse(chess.Board(fen), chess.engine.Limit(depth=depth))
        return result
    
def serialize_analysis(result):
    # Convert the POV SCore to a usable format
    score = result['score'].relative
    serialized_result = {
        'score' : score.score(),
        'mate' : score.mate(),
        'pv' : [move.uci() for move in result.get('pv', [])]
        
    }
    return serialized_result