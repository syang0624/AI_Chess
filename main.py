import threading
import pygame
import chess
from ai import get_best_move_time_limited

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
TILE_SIZE = SCREEN_WIDTH // 8
WHITE = (240, 240, 240)
GREY = (100, 100, 100)
HIGHLIGHT_COLOR = (0, 255, 0, 100)
FONT_COLOR_RED = (255, 0, 0)
FONT_COLOR_WHITE = (255, 255, 255)
FONT_COLOR_GREEN = (0, 255, 0)

PIECE_IMAGES = {}


def load_piece_images():
    """Load and scale piece images to fit the board tiles."""
    import cairosvg
    from io import BytesIO

    pieces = {
        "P": "assets/pawn-w.svg",
        "N": "assets/knight-w.svg",
        "B": "assets/bishop-w.svg",
        "R": "assets/rook-w.svg",
        "Q": "assets/queen-w.svg",
        "K": "assets/king-w.svg",
        "p": "assets/pawn-b.svg",
        "n": "assets/knight-b.svg",
        "b": "assets/bishop-b.svg",
        "r": "assets/rook-b.svg",
        "q": "assets/queen-b.svg",
        "k": "assets/king-b.svg",
    }
    for key, path in pieces.items():
        png_data = cairosvg.svg2png(url=path)
        raw_image = pygame.image.load(BytesIO(png_data))
        PIECE_IMAGES[key] = pygame.transform.scale(raw_image, (TILE_SIZE, TILE_SIZE))


def draw_board(screen, selected_square=None, possible_moves=None):
    """Draw the chessboard with optional highlights."""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GREY
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)

            if possible_moves and chess.square(col, 7 - row) in possible_moves:
                pygame.draw.circle(screen, HIGHLIGHT_COLOR, rect.center, TILE_SIZE // 4)

            if selected_square == chess.square(col, 7 - row):
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, 5)


def draw_pieces(screen, board):
    """Draw chess pieces on the board."""
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            x, y = chess.square_file(square), chess.square_rank(square)
            screen.blit(
                PIECE_IMAGES[piece.symbol()],
                (x * TILE_SIZE, (7 - y) * TILE_SIZE),
            )


def display_message(screen, message, color=FONT_COLOR_RED):
    """Display a centered message on the screen."""
    font = pygame.font.Font(None, 50)
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    )
    screen.blit(text_surface, text_rect)


def draw_button(screen, message, x, y, width, height, font_color, button_color):
    """Draw a button with text on the screen."""
    font = pygame.font.Font(None, 36)
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    text_surface = font.render(message, True, font_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return button_rect


def welcome_screen(screen):
    """Display welcome screen to choose side."""
    screen.fill((50, 50, 50))  # Dark background
    font = pygame.font.Font(None, 50)

    # Gradient rectangle
    for i in range(SCREEN_HEIGHT):
        color = (i // 5, i // 5, i // 5)  # Subtle gradient
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

    title = font.render("Choose Your Side", True, FONT_COLOR_WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    # Buttons
    white_button = draw_button(screen, "Play as White", 150, 200, 300, 50, GREY, WHITE)
    black_button = draw_button(screen, "Play as Black", 150, 300, 300, 50, GREY, WHITE)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if white_button.collidepoint(event.pos):
                    return True
                if black_button.collidepoint(event.pos):
                    return False


def main():
    pygame.init()
    load_piece_images()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Chess")
    clock = pygame.time.Clock()

    # Welcome screen
    user_plays_white = welcome_screen(screen)

    # Game state
    board = chess.Board()
    selected_square = None
    possible_moves = []
    ai_thinking = False
    game_over = False
    winner_message = ""
    user_time_left = 60
    last_time_update = pygame.time.get_ticks()  # Time tracking for updates

    def ai_thread():
        """Run the AI in a separate thread."""
        nonlocal ai_thinking, game_over, winner_message
        ai_thinking = True
        ai_move = get_best_move_time_limited(board, max_time=2.0)
        if ai_move:
            board.push(ai_move)
        ai_thinking = False

        # Check for game over
        if board.is_game_over():
            game_over = True
            result = board.result()
            if result == "1-0":
                winner_message = "White Wins!"
            elif result == "0-1":
                winner_message = "Black Wins!"
            else:
                winner_message = "Draw!"

    # If the user plays Black, let the AI make the first move
    if not user_plays_white:
        threading.Thread(target=ai_thread).start()

    running = True
    while running:
        screen.fill(GREY)

        # Update user time dynamically
        current_time = pygame.time.get_ticks()
        if board.turn == user_plays_white and not ai_thinking and not game_over:
            elapsed_time = (current_time - last_time_update) / 1000
            user_time_left -= elapsed_time
            last_time_update = current_time

            # Check if user ran out of time
            if user_time_left <= 0:
                game_over = True
                winner_message = "AI Wins! Time ran out."

        else:
            # Reset user time at the start of their turn
            if not game_over:
                user_time_left = 60
            last_time_update = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # Restart button
                    restart_button = draw_button(
                        screen, "Restart", 200, 400, 200, 50, GREY, WHITE
                    )
                    if restart_button.collidepoint(event.pos):
                        main()  # Restart the game
                        return
                elif not ai_thinking and board.turn == user_plays_white:
                    x, y = pygame.mouse.get_pos()
                    col, row = x // TILE_SIZE, 7 - (y // TILE_SIZE)
                    square = chess.square(col, row)

                    if selected_square is None:
                        selected_square = square
                        possible_moves = [
                            move.to_square
                            for move in board.legal_moves
                            if move.from_square == square
                        ]
                    else:
                        move = next(
                            (
                                m
                                for m in board.legal_moves
                                if m.from_square == selected_square
                                and m.to_square == square
                            ),
                            None,
                        )
                        if move:
                            board.push(move)

                            # Check for game over
                            if board.is_game_over():
                                game_over = True
                                result = board.result()
                                if result == "1-0":
                                    winner_message = "White Wins!"
                                elif result == "0-1":
                                    winner_message = "Black Wins!"
                                else:
                                    winner_message = "Draw!"
                            else:
                                threading.Thread(target=ai_thread).start()

                        selected_square = None
                        possible_moves = []

        draw_board(screen, selected_square, possible_moves)
        draw_pieces(screen, board)

        if ai_thinking:
            # Display "AI is thinking"
            display_message(screen, "AI is thinking...", color=FONT_COLOR_RED)
        elif not game_over:
            # Display user time left on the side
            font = pygame.font.Font(None, 36)
            user_time_text = f"Time Left: {max(0, user_time_left):.1f}s"
            user_time_surface = font.render(user_time_text, True, FONT_COLOR_GREEN)
            screen.blit(user_time_surface, (SCREEN_WIDTH - 150, 10))  # Top-right corner

        if game_over:
            display_message(screen, winner_message, color=FONT_COLOR_RED)
            restart_button = draw_button(
                screen, "Restart", 200, 400, 200, 50, GREY, WHITE
            )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
