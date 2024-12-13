from game.chess_game import ChessGame
from game.gui import draw_board, draw_pieces
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("AI Chess")
    clock = pygame.time.Clock()

    # Choose side
    print("Choose your side:")
    print("1. White")
    print("2. Black")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        user_plays_white = True
    elif choice == "2":
        user_plays_white = False
    else:
        print("Invalid choice. Defaulting to White.")
        user_plays_white = True

    game = ChessGame(user_plays_white)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and game.is_user_turn():
                x, y = pygame.mouse.get_pos()
                col, row = x // 75, 7 - (y // 75)
                square = game.get_square(col, row)
                game.user_move(square)

        if not game.is_user_turn() and not game.is_game_over():
            game.ai_move()

        # Draw the board and pieces
        draw_board(screen)
        draw_pieces(screen, game.get_board())
        pygame.display.flip()
        clock.tick(60)

        if game.is_game_over():
            print(game.get_winner())
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
