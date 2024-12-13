import time
from evaluation import evaluate_board
import chess


def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    """Minimax with Alpha-Beta Pruning."""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Prune remaining branches
        return max_eval
    else:
        min_eval = float("inf")
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Prune remaining branches
        return min_eval


def get_best_move_time_limited(board, max_time=2.0):
    """Get the best move within a given time limit."""
    start_time = time.time()
    best_move = None
    depth = 1

    # Use a copy of the board for AI calculations
    board_copy = board.copy()

    while time.time() - start_time < max_time:
        move = None
        try:
            for move in board_copy.legal_moves:
                board_copy.push(move)
                eval = minimax_alpha_beta(
                    board_copy, depth, float("-inf"), float("inf"), False
                )
                board_copy.pop()
                if best_move is None or eval > best_move[1]:
                    best_move = (move, eval)
        except Exception:
            break  # Gracefully exit if depth is too high
        depth += 1

    return best_move[0] if best_move else None
