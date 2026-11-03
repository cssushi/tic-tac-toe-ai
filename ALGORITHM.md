# Tic-Tac-Toe AI: Algorithm and Data Structures

This document explains the logic in [`tictactoe.py`](tictactoe.py), the
algorithmic core of the project. The Pygame file is only the presentation and
input layer: it draws the current board and asks this module for the next
computer move.

## 1. The problem being solved

Tic-tac-toe is a finite, deterministic, two-player, zero-sum game:

- The board always has nine positions.
- Players alternate turns.
- Every move is visible to both players.
- A player wins by occupying a complete row, column, or diagonal.
- A full board without a winner is a draw.

Because there is no randomness or hidden information, the computer can examine
the possible future states and choose a move that cannot be beaten by optimal
play. This is the classic use case for **minimax**.

## 2. Board representation

The board is represented as a nested Python list:

```python
[
    [X, O, EMPTY],
    [EMPTY, X, EMPTY],
    [O, EMPTY, EMPTY],
]
```

The outer list is the row index and the inner list is the column index. A
position is therefore addressed by a tuple `(i, j)`, where both values are
between `0` and `2`.

The module uses constants rather than repeating raw values:

- `X = "X"`
- `O = "O"`
- `EMPTY = None`

This makes comparisons explicit and avoids confusing an empty square with a
valid mark.

## 3. State transition functions

### `initial_state()`

Creates and returns a fresh 3-by-3 board containing only `EMPTY`. A new board
is produced each time a game starts or restarts.

### `player(board)`

Counts X and O marks using nested iteration. If X has more marks, O must be
next; otherwise X is next:

```python
count_x = sum(element == X for row in board for element in row)
count_o = sum(element == O for row in board for element in row)
```

This works because a valid game always has either the same number of marks or
one extra X. The function does not store a separate turn variable; it derives
the turn from the board state.

### `actions(board)`

Scans all nine cells and inserts every empty coordinate into a `set`. The set
is the collection of legal moves from the current state:

```python
{(0, 2), (1, 0), (2, 2)}
```

There are at most nine actions at the beginning of a game, decreasing after
each move.

### `result(board, action)`

Creates the next state without modifying the input state. It first validates
the coordinates, copies the board with `deepcopy`, determines the current
player, and writes that mark into the requested empty cell.

Returning a new state is important for minimax: the recursive search can
explore one hypothetical move without corrupting the board used by sibling
branches.

## 4. Detecting terminal states

### `winner(board)`

Checks the eight possible winning lines:

- 3 horizontal rows
- 3 vertical columns
- 1 main diagonal
- 1 opposite diagonal

For each line, it counts X and O values. If a line contains three X values it
returns `X`; if it contains three O values it returns `O`; otherwise it
returns `None`.

### `terminal(board)`

A state is terminal when either:

1. `winner(board)` returns a player, or
2. there are no `EMPTY` cells left.

The search must stop at terminal states. Continuing past a win would allow
the algorithm to consider impossible moves after the game has already ended.

### `utility(board)`

Converts a finished position into a numeric score from X's perspective:

| Result | Utility |
|---|---:|
| X wins | `1` |
| O wins | `-1` |
| Draw | `0` |

This is the evaluation function used at the leaves of the search tree. A
positive score is good for X, a negative score is good for O, and zero means
the result is neutral.

## 5. Minimax in `minimax(board)`

`minimax` returns a coordinate, not a score: the best legal action for the
player whose turn it is.

The function defines two recursive helpers:

### `max_value(board_max)`

This represents X's decision. X chooses the action with the largest child
value:

```python
max(min_value(result(board_max, action))
    for action in actions(board_max))
```

X tries to maximize the utility: `1` is better than `0`, and `0` is better
than `-1`.

### `min_value(board_min)`

This represents O's decision. O chooses the action with the smallest child
value:

```python
min(max_value(result(board_min, action))
    for action in actions(board_min))
```

O tries to minimize the utility because the score is always measured from X's
perspective. O prefers `-1` over `0`, and `0` over `1`.

### Root decision

At the root, the function loops through every legal action:

- If X is to move, it calls `min_value` after each candidate and keeps the
  action with the greatest score.
- If O is to move, it calls `max_value` after each candidate and keeps the
  action with the smallest score.

The special opening case returns `(1, 1)` when X is the first player on an
empty board. That is the center square, a strategically optimal opening. All
other positions are evaluated recursively.

## 6. Example of one recursive decision

Suppose X can win immediately in two different ways. For each candidate:

1. `result` creates the board after X's move.
2. `min_value` asks what O could do in response.
3. If every possible O response still leads to X winning, that branch receives
   utility `1`.
4. X compares the returned values and selects the highest one.

If a move allows O to win, the branch eventually returns `-1`, so X avoids it
when a safer branch exists. This is how the algorithm reasons about threats
without using a hand-written list of tactical rules.

## 7. Complexity and data-structure analysis

At an empty board, the branching factor is at most 9, then 8, then 7, and so
on. In the general minimax model, the time complexity is approximately
`O(b^d)`, where `b` is the branching factor and `d` is the remaining depth.
For tic-tac-toe, `b <= 9` and `d <= 9`, so the complete game tree is small
enough to search directly.

The recursion uses `O(d)` call-stack space. In addition, each `result` call
creates a copied 3-by-3 board, which is constant-sized for this game. The
implementation does not memoize repeated states, so equivalent board states
can be recalculated through different move orders.

The main data structures are deliberately simple:

- nested lists for mutable board storage
- tuples for coordinate actions
- a set for the available-action collection
- recursion for the depth-first game-tree traversal

## 8. Design trade-offs and limitations

- **No alpha-beta pruning:** every reachable continuation is evaluated. This is
  easy to read for a course project, but alpha-beta pruning would reduce the
  number of branches explored without changing the answer.
- **No memoization:** the same board can be reached through different move
  sequences and is recalculated. A transposition table keyed by an immutable
  board representation could improve efficiency.
- **Scores are not depth-sensitive:** a win and a loss are valued only as `1`
  and `-1`. The AI does not explicitly prefer a faster win or a slower loss.
- **Action ordering comes from a set:** when multiple actions have equal
  utility, the selected move can depend on set iteration order. The result is
  still optimal even if the visual move differs between equivalent choices.

Despite these trade-offs, the implementation is correct for the game: with
perfect play, minimax prevents the computer from choosing a move that leads to
an avoidable loss.

## 9. Where the visuals fit

`runner.py` maintains the current board and delegates all game decisions to
this module. It calls `initial_state`, `player`, `result`, `terminal`, and
`minimax`; it does not duplicate the rules. The visual layer renders the
board state, highlights available cells, and communicates whether the user or
the AI is thinking.
