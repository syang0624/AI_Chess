# AI Chess Game

This is a simple chess application featuring a graphical interface built with Pygame and a time-limited AI opponent powered by a minimax algorithm and alpha-beta pruning. The AI evaluation is rudimentary and evaluates positions from White’s perspective.

## Features

-   **Graphical Board:** The game provides a familiar, easy-to-use chessboard interface powered by Pygame.
-   **Play as White or Black:** Choose your side at the start and let the AI make the first move if you opt to play as Black.
-   **AI Opponent:** The AI uses a minimax-based algorithm with alpha-beta pruning. It searches within a fixed time limit to find a good move.
-   **Time Control:** The player has a limited amount of time (60 seconds) per move. If you run out of time, the AI automatically wins.
-   **Game Over Detection:** The program displays the game result (White wins, Black wins, or draw) at the end of the match and offers a restart button.

## Requirements

-   Python 3.7+
-   Pygame
-   python-chess
-   cairosvg

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

## Virtual Environment Setup

It’s generally good practice to run projects within a dedicated virtual environment to avoid conflicts with system-wide packages. Here’s how to set one up:

1. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    ```

    This creates a virtual environment folder named `venv` in your project directory.

2. **Activate the virtual environment:**
    - On Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application while in the virtual environment:**
    ```bash
    python main.py
    ```

When you’re done, you can deactivate the virtual environment by running:

```bash
deactivate
```

## Files

-   **main.py:** Entry point of the application, handles the GUI, event loop, user input, and integration with the AI.
-   **ai.py:** Contains the AI logic, including the time-limited best move search and the minimax with alpha-beta pruning algorithm.
-   **evaluation.py:** Defines the evaluation function used by the AI to score board positions.
-   **assets/:** Directory containing SVG pieces used to render the chess pieces on the board.

    **Note:** The chess piece images were adapted from [GreenChess (https://greenchess.net/info.php?item=downloads)](https://greenchess.net/info.php?item=downloads).

## How to Run

1. **(Optional) Set up and activate a virtual environment** as described above.
2. Start the game:
    ```bash
    python main.py
    ```
3. Choose your side when prompted.
4. Make moves by clicking on pieces and their possible destination squares.

## Gameplay Instructions

-   **Selecting and Moving Pieces:**  
    Click on a piece to select it. Potential moves are highlighted by green dots on the target squares. Click a highlighted square to move.

-   **Time Management:**  
    Your current remaining time is displayed in the top-right corner. Make your move before the time runs out.

-   **AI Thinking:**  
    When it’s the AI’s turn, “AI is thinking...” appears on the screen. Wait for the AI to make its move.

-   **Game Over:**  
    When the game ends (checkmate, draw, or time out), a message displays the result. Click “Restart” to start a new game.

## Improving the AI

The current AI uses a basic evaluation function and a simple iterative deepening approach with a fixed time limit. You can improve it by:

-   Enhancing the evaluation function (e.g., better piece-square tables, king safety, pawn structure).
-   Implementing more sophisticated search techniques (iterative deepening, transposition tables, quiescence search).
-   Adjusting time management strategies or integrating a more complex engine.
