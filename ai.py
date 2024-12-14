import time
import chess
import random
from evaluation import evaluate_board

# Zobrist hashing setup
ZOBRIST_PIECE_KEYS = {}
ZOBRIST_CASTLING_KEYS = {}
ZOBRIST_EP_KEYS = {}
ZOBRIST_SIDE_TO_MOVE_KEY = 0
transposition_table = {}


def initialize_zobrist():
    global ZOBRIST_PIECE_KEYS, ZOBRIST_CASTLING_KEYS, ZOBRIST_EP_KEYS, ZOBRIST_SIDE_TO_MOVE_KEY
    random.seed(42)
    ZOBRIST_PIECE_KEYS = {
        (square, piece): random.getrandbits(64)
        for square in range(64)
        for piece in [
            chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING,
            chess.PAWN + 6, chess.KNIGHT + 6, chess.BISHOP + 6, chess.ROOK + 6, chess.QUEEN + 6, chess.KING + 6
        ]
    }
    ZOBRIST_CASTLING_KEYS = {right: random.getrandbits(64) for right in range(16)}
    ZOBRIST_EP_KEYS = {file_: random.getrandbits(64) for file_ in range(8)}
    ZOBRIST_SIDE_TO_MOVE_KEY = random.getrandbits(64)


def compute_zobrist_hash(board):
    h = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_code = piece.piece_type if piece.color else piece.piece_type + 6
            h ^= ZOBRIST_PIECE_KEYS[(square, piece_code)]

    if board.turn == chess.BLACK:
        h ^= ZOBRIST_SIDE_TO_MOVE_KEY

    c_val = 0
    if board.has_kingside_castling_rights(chess.WHITE):
        c_val |= 1
    if board.has_queenside_castling_rights(chess.WHITE):
        c_val |= 2
    if board.has_kingside_castling_rights(chess.BLACK):
        c_val |= 4
    if board.has_queenside_castling_rights(chess.BLACK):
        c_val |= 8

    h ^= ZOBRIST_CASTLING_KEYS[c_val]

    if board.ep_square is not None:
        file_ = chess.square_file(board.ep_square)
        h ^= ZOBRIST_EP_KEYS[file_]

    return h


initialize_zobrist()


def lookup_transposition(hash_key, alpha, beta, depth):
    if hash_key in transposition_table:
        stored_depth, stored_value, stored_flag = transposition_table[hash_key]
        if stored_depth >= depth:
            if stored_flag == "EXACT":
                return stored_value
            elif stored_flag == "ALPHA" and stored_value <= alpha:
                return alpha
            elif stored_flag == "BETA" and stored_value >= beta:
                return beta
    return None


def store_transposition(hash_key, depth, value, flag):
    transposition_table[hash_key] = (depth, value, flag)


def order_moves(board):
    """Order moves to improve alpha-beta efficiency.
    Simple heuristic: put captures and checks first."""
    moves = list(board.legal_moves)
    def move_score(move):
        # captures
        if board.is_capture(move):
            return 2
        # checks
        board.push(move)
        in_check = board.is_check()
        board.pop()
        if in_check:
            return 1
        return 0
    moves.sort(key=move_score, reverse=True)
    return moves


def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    hash_key = compute_zobrist_hash(board)
    tt_val = lookup_transposition(hash_key, alpha, beta, depth)
    if tt_val is not None:
        return tt_val

    if maximizing_player:
        max_eval = float("-inf")
        stored_flag = "ALPHA"
        moves = order_moves(board)
        for move in moves:
            board.push(move)
            eval_ = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval_ > max_eval:
                max_eval = eval_
            alpha = max(alpha, eval_)
            if beta <= alpha:
                break
        if max_eval <= alpha:
            stored_flag = "ALPHA"
        elif max_eval >= beta:
            stored_flag = "BETA"
        else:
            stored_flag = "EXACT"
        store_transposition(hash_key, depth, max_eval, stored_flag)
        return max_eval
    else:
        min_eval = float("inf")
        stored_flag = "BETA"
        moves = order_moves(board)
        for move in moves:
            board.push(move)
            eval_ = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval_ < min_eval:
                min_eval = eval_
            beta = min(beta, eval_)
            if beta <= alpha:
                break
        if min_eval <= alpha:
            stored_flag = "ALPHA"
        elif min_eval >= beta:
            stored_flag = "BETA"
        else:
            stored_flag = "EXACT"
        store_transposition(hash_key, depth, min_eval, stored_flag)
        return min_eval


def get_best_move_time_limited(board, max_time=2.0):
    analysis_board = board.copy()
    start_time = time.time()
    best_move = None
    maximizing_player = analysis_board.turn
    depth = 1

    while time.time() - start_time < max_time:
        current_best_move = None
        current_best_eval = float("-inf") if maximizing_player else float("inf")
        try:
            moves = order_moves(analysis_board)
            for move in moves:
                analysis_board.push(move)
                eval_ = minimax_alpha_beta(analysis_board, depth - 1, float("-inf"), float("inf"), not maximizing_player)
                analysis_board.pop()
                if maximizing_player and eval_ > current_best_eval:
                    current_best_eval = eval_
                    current_best_move = move
                elif not maximizing_player and eval_ < current_best_eval:
                    current_best_eval = eval_
                    current_best_move = move
        except Exception:
            break

        if current_best_move is not None:
            best_move = current_best_move

        depth += 1
        if time.time() - start_time >= max_time:
            break

    return best_move
