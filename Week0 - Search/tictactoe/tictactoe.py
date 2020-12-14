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
    # Counts X and O in the board.
    count_of_X = sum(row.count(X) for row in board)
    count_of_O = sum(row.count(O) for row in board)

    # If X is greater than O, it returns O.
    # Since X plays first, it'll always have atleast no. of O
    if count_of_X > count_of_O:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Initialize empty set of actions.
    actions = set()

    # Iterates through the board and adds EMPTY cells to the actions set.
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    # Returns set of all possible actions on the board.
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if terminal(board) or action not in actions(board):
        raise Exception("Invalid Move.")

    # Since set is not subscriptable, storing it's values in 2 variables.
    i, j = action

    # The transition state of the board is calculated.
    tmp_board = deepcopy(board)
    tmp_board[i][j] = player(board)

    # Returns the transition state of the board.
    return tmp_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Iterates through the rows and finds winning patterns.
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] is not None:
            return board[i][0]

    # Iterates through the columns and finds winning patterns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] is not None:
            return board[0][i]

    # Checks for diagonal winning patterns
    if board[0][0] == board[2][2] == board[1][1] is not None:
        return board[1][1]

    if board[2][0] == board[0][2] == board[1][1] is not None:
        return board[1][1]

    # If none of the conditions above are met, there are no winners.
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If someone won, returns True.
    if winner(board) is not None:
        return True

    # If the board is full, returns True.
    if sum(row.count(EMPTY) for row in board) == 0:
        return True

    # Else, the game is still going on.
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Creating a dictionary with values for each scenario.
    value = {X: 1, O: -1, None: 0}

    # Returns corresponding value from dictionary.
    return value[(winner(board))]


def MAXV(board):
    """
    Returns the maximum value at that state.
    """
    # If the game is over, the only possible value
    # will be the value at that state.
    if terminal(board):
        return utility(board)

    # Initializing v as the minimum possible value.
    v = -math.inf

    # Iterates through all the actions in board and
    # checks for the maximum value recursively.
    for action in actions(board):
        v = max(v, MINV(result(board, action)))

        # In this game, the maximum value is 1.
        if v == 1:
            return v

    return v


def MINV(board):
    """
    Returns the minimum value at that state.
    """
    # If the game is over, the only possible value will be
    # the value at that state
    if terminal(board):
        return utility(board)

    # Initializing v as the maximum possible value.
    v = math.inf

    # Iterates through all the actions in board and
    # checks for the minimum value recursively.
    for action in actions(board):
        v = min(v, MAXV(result(board, action)))

        # In this game, the minimum value is 1.
        if v == -1:
            return v

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If terminal board, returns None.
    if terminal(board):
        return None

    # Getting set of all possible actions.
    possible_actions = actions(board)

    """
    # The first round is computationally expensive, so this makes it "faster".
    # The AI always plays at (0, 1) given first move.
    if board == initial_state():
        return (0, 1)
    """

    # Initialize a set variable to store optimal action in.
    optimal_action = set()

    # If it's X player's turn. X wants to maximize the result.
    if player(board) == X:
        # Initialize a temporary variable to compare v against.
        tmp = -math.inf
        # Checking MIN values for each action.
        for action in possible_actions:
            v = MINV(result(board, action))
            if v > tmp:
                tmp = v
                optimal_action = action
            # The maximum possible value in this game is 1.
            if tmp == 1:
                return action

        return optimal_action

    # If it's O player's turn. O wants to maximize the result.
    else:
        # Initialize a temporary variable to compare v against.
        tmp = math.inf
        # Checking MAX values for each action.
        for action in possible_actions:
            v = MAXV(result(board, action))
            if v < tmp:
                tmp = v
                optimal_action = action
            # The minimum possible value in this game is -1.
            if tmp == -1:
                return action

        return optimal_action
