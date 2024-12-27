from flask import Blueprint, request, jsonify
from controllers.analysis_controller import analyze_game

analysis_bp = Blueprint('analysis_bp', __name__)

@analysis_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    fen = data['fen']
    depth = data.get('depth', 15)
    result = analyze_game(fen, depth)
    return jsonify(result), 200