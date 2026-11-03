# Tic-Tac-Toe AI

A Pygame tic-tac-toe game where you play against a computer opponent.

## Setup

1. Install the dependency:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

2. Start the game:

   ```bash
   python3 runner.py
   ```

Choose whether to play as X or O, then click an empty square to make a move.

## How it works

- [`runner.py`](runner.py) initializes Pygame, draws the menus and board, handles mouse input, and alternates between the human and computer turns.
- [`tictactoe.py`](tictactoe.py) contains the game rules:
  - `initial_state` creates an empty board.
  - `player` determines whose turn is next.
  - `actions` lists available squares.
  - `result` returns a new board after a move.
  - `winner`, `terminal`, and `utility` evaluate the position.
  - `minimax` searches possible future moves and chooses an optimal move for the computer.
- `OpenSans-Regular.ttf` provides the font used by the Pygame interface.

The minimax algorithm assumes X is the maximizing player and O is the minimizing player. It recursively evaluates every possible continuation, selecting moves that lead to a win when possible and avoiding losses.

## Controls

- Click **Play as X** or **Play as O** to begin.
- Click an empty square to place your mark.
- Click **Play Again** after a game ends.
- Close the game window to exit.
