"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np
import pandas as pd

X = "X"
O = "O"
EMPTY = None
bs = 3


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
    if (board == initial_state()) | ((pd.notna(board).sum())%2 == 0):
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = []
    for i in range(bs):
        for j in range(bs):
            if pd.isna(board[i][j]):
                all_actions.append((i,j))
    return all_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    nboard = copy.deepcopy(board)
    assert pd.isna(nboard[action[0]][action[1]])==True, "Invalid action"
    nboard[action[0]][action[1]] = player(board)
    return nboard




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if ([board[i][i] for i in range(bs)]==[X,X,X]) | ([board[i][bs-i-1] for i in range(bs)]==[X,X,X]): 
        return X
    elif ([board[i][i] for i in range(bs)]==[O,O,O]) | ([board[i][bs-i-1] for i in range(bs)]==[O,O,O]): 
        return O
    for i in range(bs):
        if (board[i]==[X,X,X]) | ([v[i] for v in board]==[X,X,X]):
            return X
        if (board[i]==[O,O,O]) | ([v[i] for v in board]==[O,O,O]):
            return O
    return None




def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (pd.isna(board).sum()==0) | (winner(board)!=None):
        return True
    else:
        return False





def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
        return 1
    elif winner(board)==O:
        return -1
    else:
        return 0


## define the two recursive funcs to be used later 

def MAX_VALUE(board):
    if terminal(board):         
        return utility(board), None 
    v = -np.inf 
    for action in actions(board): 
        nboard = result(board, action)
        if MIN_VALUE(nboard)[0] > v:
            v = MIN_VALUE(nboard)[0]
            final_action = action
  
    return v, final_action

def MIN_VALUE(board):
    if terminal(board):
        return utility(board), None 
    v = np.inf  
    for action in actions(board):
        nboard = result(board, action)
        if MAX_VALUE(nboard)[0] < v:
            v = MAX_VALUE(nboard)[0]
            final_action = action

    return v, final_action

## TODO: main function change to board with bigger size 
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board)==X:
        v, final_action = MAX_VALUE(board)
    else:
        v, final_action = MIN_VALUE(board)
    return final_action
