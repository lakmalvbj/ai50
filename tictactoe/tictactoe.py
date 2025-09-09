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
    no_of_x = sum(i.count(X) for i in board) 
    if(no_of_x == 0):
        return X
    no_of_o = sum(i.count(O) for i in board) 
    if(no_of_o < no_of_x):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions =list()
    for i,x in enumerate(board):
        for j,o in enumerate(x):
            if(o == EMPTY):
                actions.append((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)
    new_board =  deepcopy(board)
    new_board[action[0]][action[1]] = current_player
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """ 
    level = len(board)  
    diagnol_top = []
    diagnol_bottom = []
    for i in range(level):  
        diagnol_top.append(board[i][i]) 
        diagnol_bottom.append(board[i][level - (i + 1)]) 
        first_col = board[i][0]
        column = ([row[i] for row in board])
        first_row = column[0]
        if(first_row != None and all(first_row == j for j in column)):
            return first_row
        if(first_col != None and all(first_col == j for j in board[i])):
            return first_col
    first_diagnol_top = diagnol_top[0]
    if(first_diagnol_top != None and all(first_diagnol_top == j for j in diagnol_top)):
        return first_diagnol_top
    first_diagnol_bottom = diagnol_bottom[0]
    if(first_diagnol_bottom != None and all(first_diagnol_bottom == j for j in diagnol_bottom)):
        return first_diagnol_bottom 

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) != None or len(actions(board)) == 0

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    if winning_player == X:
        return 1
    if winning_player == O:
        return -1
    return 0

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """     
    if terminal(board):
       return None
    
    next_action = None
    current_player = player(board)
    if current_player == X:
        max = -math.inf
        for action in actions(board):
            print(action)
            next_value = min_value(result(board, action))
            if next_value > max:
                max = next_value
                next_action = action
     
    else:
        min = math.inf
        for action in actions(board):
            next_value = max_value(result(board, action))
            if next_value < min:
                min = next_value 
                next_action = action
    
    return next_action

