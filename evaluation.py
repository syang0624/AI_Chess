import chess


def evaluate_board(board):
    """Efficiently evaluate the board position."""
    piece_values = {
        "p": -1,
        "n": -10,
        "b": -100,
        "r": -1000,
        "q": -10000,
        "k": 0,
        "P": 1,
        "N": 10,
        "B": 100,
        "R": 1000,
        "Q": 10000,
        "K": 0,
    }
    value = 0

    # Material evaluation
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value += piece_values[piece.symbol()]

    # Center control: Reward central squares
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    for square in center_squares:
        piece = board.piece_at(square)
        if piece:
            value += 0.5 if piece.color else -0.5

    # Mobility: Reward number of legal moves
    legal_moves = list(board.legal_moves)
    value += 0.1 * len(legal_moves) if board.turn else -0.1 * len(legal_moves)

    return value
