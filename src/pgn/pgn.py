import chess.pgn
import io

def parse_pgn(pgn):
    pgn_io = io.StringIO(pgn)   
    game = chess.pgn.read_game(pgn_io)
    return game

def process_moves(pgn, san_only = False):
    game = parse_pgn(pgn)
    board = game.board()
    san_moves = []
    fens = []
    uci_moves = []
    
    if san_only:
            for move in game.mainline_moves():
                san_moves.append(board.san(move))
                board.push(move)
                fens.append(board.fen())
            return san_moves, fens
    else:
            for move in game.mainline_moves():
                san_moves.append(board.san(move))
                board.push(move)
                uci_moves.append(move.uci())
                fens.append(board.fen())
            return uci_moves, san_moves, fens

def convert_movelist_to_pgn(moves):
    pgn = ""
    move_number = 1

    for move in moves:
        if move_number % 2 == 1:
            pgn += f"{move_number // 2 + 1}.{move} "
        else:
            pgn += f"{move} "
        move_number += 1

    return pgn.strip()