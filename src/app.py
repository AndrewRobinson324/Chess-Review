import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template
import logging
from routes.game_routes import game_bp
from routes.analysis_routes import analysis_bp
from controllers.game_controller import save_game, get_games
from controllers.game_controller import get_game_by_id

app = Flask(__name__)
app.debug = True

# configure logger for more detailed output
logging.basicConfig(level=logging.INFO)

app.register_blueprint(game_bp)
app.register_blueprint(analysis_bp)

@app.route('/')
def index():
    app.logger.info('Index page requested')
    return render_template('index.html')

# add a route to get a single game
@app.route('/games/<game_id>', methods=['GET'])
def game_analysis(game_id):
    game = get_game_by_id(game_id)
    pgn = game['pgn']
    
    if game:
        return render_template('game_analysis_page.html', pgn=pgn)
    else: 
        return 'Game not found', 404

if __name__ == '__main__':
    app.run(debug=True)