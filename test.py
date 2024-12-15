import unittest
import chess
from evaluation import evaluate_board
from ai import get_best_move_time_limited

class TestChessAI(unittest.TestCase):

    def test_evaluation_returns_numeric(self):
        board = chess.Board()
        score = evaluate_board(board)
        self.assertIsInstance(score, (int, float), "Evaluation should return a numeric value")

    def test_ai_move_in_start_position(self):
        board = chess.Board()
        move = get_best_move_time_limited(board, max_time=1.0)
        # The AI should return a legal move
        self.assertIsNotNone(move, "AI should return a legal move from the starting position")
        self.assertIn(move, board.legal_moves, "Returned move must be legal in the current board state")

    def test_ai_move_in_midgame_position(self):
        # A midgame position (example: after some random moves)
        board = chess.Board()
        moves = ["e4", "e5", "Nf3", "Nc6", "Bb5", "Nf6", "O-O", "Nxe4", "Re1", "Nd6", "Nxe5"]
        for m in moves:
            board.push_san(m)

        move = get_best_move_time_limited(board, max_time=1.0)
        self.assertIsNotNone(move, "AI should return a legal move from a midgame position")
        self.assertIn(move, board.legal_moves, "Returned move must be legal from the midgame position")

    def test_repeated_calls_same_position(self):
        # Test that calling the AI multiple times doesn't cause errors and remains consistent
        board = chess.Board()
        for _ in range(3):
            move = get_best_move_time_limited(board, max_time=1.0)
            self.assertIsNotNone(move, "AI should consistently return moves on repeated calls")
            self.assertIn(move, board.legal_moves, "Returned move must be legal each time")

    def test_no_moves_game_over(self):
        # A checkmate position: black king is checkmated in a famous puzzle position
        # One well-known mate: White to move and mate (Fool's mate)
        board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1")
        # Position after "f3 e5 g4 Qh4#" - Black checkmates White
        # Let's create that position:
        board.clear()
        board.set_fen("rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq - 0 2")
        # Black's move Qh4#:
        board.push_uci("d8h4") # Checkmate now.
        self.assertTrue(board.is_game_over(), "Position should be a checkmate")

        move = get_best_move_time_limited(board, max_time=1.0)
        self.assertIsNone(move, "No move should be returned in a checkmate position")

    def test_ai_performance_under_time_constraints(self):
        # Test AI performance under very short time constraints
        board = chess.Board()
        move = get_best_move_time_limited(board, max_time=0.1)
        self.assertIsNotNone(move, "AI should return a move even with very short time constraints")
        self.assertIn(move, board.legal_moves, "Returned move must be legal even under time pressure")

    def test_ai_move_after_check(self):
        # Test AI response after a check
        board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1")
        board.push_san("f3")  # White plays f3
        board.push_san("e5")  # Black plays e5
        board.push_san("g4")  # White plays g4
        board.push_san("Qh4+")  # Black gives check
        move = get_best_move_time_limited(board, max_time=1.0)
        self.assertIsNotNone(move, "AI should return a move after a check")
        self.assertIn(move, board.legal_moves, "Returned move must be legal after a check")

    def test_ai_handles_stalemate(self):
        # Test AI response in a stalemate position
        board = chess.Board("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")  # Black is in stalemate
        self.assertTrue(board.is_stalemate(), "The position should be a stalemate")
        move = get_best_move_time_limited(board, max_time=1.0)
        self.assertIsNone(move, "AI should not return a move in a stalemate position")

if __name__ == "__main__":
    unittest.main()
