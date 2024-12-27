from analysis.stockfish import analyze_game as stockfish_analyze

def analyze_game(fen, depth):
    return stockfish_analyze(fen, depth)