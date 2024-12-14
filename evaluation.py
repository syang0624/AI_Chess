import chess

# Improved piece values
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0
}

# Piece-square tables (from a White perspective)
PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5, 10, 10, 10, 10,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -10,  5,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
]


def piece_square_value(piece, square):
    """Get piece-square table value for a given piece."""
    row = 7 - chess.square_rank(square)
    col = chess.square_file(square)
    index = row * 8 + col

    tables = {
        chess.PAWN: PAWN_TABLE,
        chess.KNIGHT: KNIGHT_TABLE,
        chess.BISHOP: BISHOP_TABLE,
        chess.ROOK: ROOK_TABLE,
        chess.QUEEN: QUEEN_TABLE,
        chess.KING: KING_TABLE
    }

    base = tables[piece.piece_type][index]
    # For black pieces, invert perspective
    return base if piece.color == chess.WHITE else -base


def evaluate_board(board):
    """
    More nuanced board evaluation:
    - Material
    - Piece-square placement
    - Mobility
    - Center control
    - Basic king safety approximation
    """
    if board.is_game_over():
        # If game is over, evaluation should reflect results
        if board.is_checkmate():
            return float("inf") if board.turn == chess.BLACK else float("-inf")
        else:
            return 0.0  # draw

    value = 0.0

    # Material and position
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # Material
            piece_val = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.BLACK:
                piece_val = -piece_val
            value += piece_val

            # Piece-square table
            value += piece_square_value(piece, square)

    # Mobility
    legal_moves = list(board.legal_moves)
    mobility = len(legal_moves)
    if board.turn == chess.WHITE:
        value += 0.1 * mobility
    else:
        value -= 0.1 * mobility

    # Center control
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    for sq in center_squares:
        piece = board.piece_at(sq)
        if piece:
            if piece.color == chess.WHITE:
                value += 0.3
            else:
                value -= 0.3

    # King safety (very simplistic)
    white_king_pos = board.king(chess.WHITE)
    black_king_pos = board.king(chess.BLACK)
    if white_king_pos is not None:
        wr, wf = divmod(white_king_pos, 8)
        wc_dist = abs(wf - 3.5) + abs(wr - 3.5)
        value -= wc_dist * 0.05
    if black_king_pos is not None:
        br, bf = divmod(black_king_pos, 8)
        bc_dist = abs(bf - 3.5) + abs(br - 3.5)
        value += bc_dist * 0.05

    return value
