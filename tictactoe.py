"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    # player whose turn has less marks 

    count_x = sum(element == X for row in board for element in row)
    count_o = sum(element == O for row in board for element in row)

    if count_x > count_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()

    for i in range(len(board)):
        for j in range(len(board)):

            # check if empty
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    i, j = action

    if i not in range(3) or j not in range(3):
        raise ValueError("Invalid Action")
    
    other = deepcopy(board)

    if board[i][j] is EMPTY:
        other[i][j] = player(board)
    else:
        raise ValueError("Invalid Action")

    return other


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # horizontal, vertical or diagonal same

    # horizontal, check for element in row all same
    # vertical, check for same row, change column, all same
    # diagonal, row == col and, row = 0, col = max, row += 1: col -= 1

    # horizontal
    for i in range(len(board)):
        if sum(board[i][j] == X for j in range(len(board))) == len(board):
            return X
        elif sum(board[i][j] == O for j in range(len(board))) == len(board):
            return O

    # vertical
    for i in range(len(board)):
        if sum(board[j][i] == X for j in range(len(board))) == len(board):
            return X
        elif sum(board[j][i] == O for j in range(len(board))) == len(board):
            return O

    # diagonal
    # first diagonal
    if sum(board[i][i] == X for i in range(len(board))) == len(board):
        return X
    elif sum(board[i][i] == O for i in range(len(board))) == len(board):
        return O

    # second diagonal
    j = len(board) - 1

    if sum(board[i][j - i] == X for i in range(len(board))) == len(board):
        return X
    elif sum(board[i][j - i] == O for i in range(len(board))) == len(board):
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # game over if
    # someone won
    # all spots taken

    # check if winner
    if winner(board):
        return True

    # implement all spots taken
    if sum(element is EMPTY for row in board for element in row) == 0:
        # all spots taken
        return True

    # spots left and no winner
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # only runs if terminal true

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """

    if terminal(board):
        return None

    # if bot playing first
    if player(board) == X and all(element is EMPTY for row in board for element in row):
        return (1, 1)


#     max_player = player(board)

#     def min_value(board_min):
        
#         if terminal(board_min):
#             return utility(board_min)
#         else:
#             actions_min = actions(board_min)
#             print("Actions min:", actions_min)

#             value = math.inf
#             min_action = actions_min[0]
#             for i in range(len(actions_min)):
#                 curr_val = max_value(result(board_min, actions_min[i]))
#                 if curr_val < value:
#                     min_action = actions_min[i]

#             return min_action
#             # return min(max_value(result(board_min, action_min)) for action_min in actions_min)

        
#     def max_value(board_max):

#         if terminal(board_max):
#             return utility(board_max)
#         else:
#             actions_max = actions(board_max)
#             print("Actions_max:", actions_max)

#             value = -math.inf
#             max_action = actions_max[0]
#             for i in range(len(actions_max)):
#                 curr_val = min_value(result(board_max, actions_max[i]))
#                 if curr_val > value:
#                     max_action = actions_max[i]

#             return max_action

#             # return max(min_value(result(board_max, action_max)))

#     return max_value(board)
    def max_value(board_max):
        if terminal(board_max):
            return utility(board_max)
        else:
            return max(min_value(result(board_max, action_max)) for action_max in actions(board_max))

    def min_value(board_min):
        if terminal(board_min):
            return utility(board_min)
        else:
            return min(max_value(result(board_min, action_min)) for action_min in actions(board_min))
    



    # given state s
        ## max player picks action a in actions that produce highest value in min-value(results(s, a))

        ## min player picks action a in actions that produce lowest value in max-value(results(s, a))

        ## results(s, a) == set of results after action a on state s

    # max_player = player(board)
    # player_actions = actions(board)

    # return max(min_value(minimax_result) for )
    
    # initial value
    # value = min_value(result(board, player_actions[0]))

    if player(board) == X:

        value = -math.inf

        for action in actions(board):

            new_value = min_value(result(board, action))

            if new_value > value:
                value = new_value
                best_action = action

        return best_action
    else:

        value = math.inf

        for action in actions(board):
            
            new_value = max_value(result(board, action))

            if new_value < value:
                value = new_value
                best_action = action

        return best_action

    # for action in player_actions:
    #     max(    

    #         this is a set of min-value results
    #         mapped with actoin

    #     )


    # results_player = result(board, actions(board))




    # function max-value:
        ## v = -inf , math.inf
        ## if terminal, return utility
        ## or for action in actions(state) (for every action avail in state)
            ### v, value = Max(v, min-value(result(state, action)))
            ### return v and action assos with v


    # function min-value:
        ## v = +inf
        ## if terminal, return utility
        ## or for action in actions(state)
            ### v = Min(v, max-value(result(state, action)))
        ### return v and action assos w v
