from flask import Blueprint, request, jsonify, render_template
from controllers.game_controller import save_game, get_games, get_game_by_id
from analysis.stockfish import analyze_game as stockfish_analyze
from pgn.pgn import parse_pgn, process_moves, convert_movelist_to_pgn
import chess.pgn


game_bp = Blueprint('game_bp', __name__)

@game_bp.route('/games', methods=['POST'])
def add_game():
    data = request.json
    pgn = data['pgn']
    
    # Parse the PGN and process the moves
    game = parse_pgn(pgn)
    if game is None:
        return jsonify({'message': 'Failed to parse PGN'}), 400
    
    uci_moves, san_moves, fens = process_moves(pgn)
    analysis = []
    
    # Analyze each move using Stockfish
    for fen in fens:
        print(f"Analyzing FEN: {fen}")
        try:
            analyzed_moves = stockfish_analyze(fen, depth=15, multi_pv=3)  # Analyze with multiple PVs
            analysis.extend(analyzed_moves)  # Add all PVs to the analysis
        except Exception as e:
            print(f"Error analyzing FEN {fen}: {e}")
            return jsonify({'message': f'Error analyzing FEN {fen}: {e}'}), 400
    
    # Save the game and analysis to the database
    try:
        #print(f"Saving game with analysis: {analysis}")
        game_id = save_game(pgn, analysis)
        print(f"Game saved with ID: {game_id}")  # Add logging
    except Exception as e:
        print(f"Error saving game: {e}")
        return jsonify({'message': f'Error saving game: {e}'}), 500
    
    # Respond with the game ID
    return jsonify({'game_id': str(game_id)}), 201

@game_bp.route('/games', methods=['GET'])
def list_games():
    games = get_games()
    return jsonify(games), 200

# add a route to get a single game by id
@game_bp.route('/games/<game_id>', methods=['GET'])
def get_game(game_id):
    game = get_game_by_id(game_id)
    if game:
        return render_template('game_analysis_page.html', pgn=game['pgn'])
    else:
        return 'Game not found', 404