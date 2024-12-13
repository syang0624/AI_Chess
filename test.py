import chess
from ai import get_best_move
from evaluation import evaluate_board


def test_ai():
    board = chess.Board()
    print("Initial Board:")
    print(board)
    move = get_best_move(board, depth=4)  # Fixed argument
    print("AI Move:", move)


def test_evaluation():
    board = chess.Board()
    print("Evaluation Score:", evaluate_board(board))


if __name__ == "__main__":
    test_ai()
    test_evaluation()
