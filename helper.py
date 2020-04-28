"""
Tic Tac Toe Player
"""

from math import inf
import copy

X = "X"
O = "O"
EMPTY = ""


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
    X_num = 0
    O_num = 0
    EMPTY_num = 0
    for row in board:
        X_num += row.count(X)
        O_num += row.count(O)
        EMPTY_num += row.count(EMPTY)

    # print(X_num, O_num, EMPTY_num)

    if EMPTY_num == 0:
        return 
    elif X_num == 0 and O_num == 0:
        return X
    elif X_num == O_num:
        return X
    elif X_num > O_num:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    options = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                options.add((i, j))
    return options


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    options = actions(board)
    if (i, j) not in options:
        raise ValueError("Invalid action")

    res = copy.deepcopy(board)
    pl = player(board)
    res[i][j] = pl
    return res


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win_state = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    # pl = player(board)
    if [X, X, X] in win_state:
        return X
    elif [O, O, O] in win_state:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or player(board) is None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    res = winner(board)
    if res == X:
        return 1
    elif res == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    pl = player(board)

    if terminal(board):
        score = utility(board)
        return [(-1, -1), score]

    if pl == O:
        best = [(-1, -1), inf]
    elif pl == X:
        best = [(-1, -1), -inf]

    for i, j in actions(board):
        res = result(board, (i, j))
        score = minimax(res)
        score[0] = (i, j)

        if pl == O:
            if score[1] < best[1]:
                best = score
        elif pl == X:
            if score[1] > best[1]:
                best = score
    return best