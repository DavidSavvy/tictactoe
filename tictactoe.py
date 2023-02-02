"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
from pickle import NONE
import random
from typing import final

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
    moves = 0
    for row in board:
        for col in row:
            if col != EMPTY: moves += 1
                   
    if moves == 0 or moves % 2 == 0:
        return X
    else:
        return O
   

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for row_idx, row in enumerate(board):
        for col_idx, col in enumerate(row):
            if col == EMPTY:
                possible_actions.add((row_idx, col_idx))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = deepcopy(board)
    if board_copy[action[0]][action[1]] == EMPTY:
        board_copy[action[0]][action[1]] = player(board)
        return board_copy
    else:
        raise Exception("invalid action")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    current_player = None
    if player(board) == X:
        current_player = O
    else:
        current_player = X
    
    # Checks rows and columns for winner
    for i in range(0,3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY or board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return current_player
    
    # Checks diagonals for winner
    if board[0][0] == board[1][1] == board[2][2] != EMPTY or board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return current_player
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    possible_actions = actions(board)
    if len(possible_actions) == 0 or winner(board) != None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if terminal(board):
        return None
    
    def min_function(working_board):
        min_value = 1
        # Ends recursion to go up the call stack
        if terminal(working_board):
            return utility(working_board)
        else:
            # Recurses back to opposite function for every possible move
            for action in actions(working_board):
                min_value = min(min_value, max_function(result(working_board, action)))
                # Short alpha-beta prune, to stop when reached lowest value, saves recursion time
                if min_value == -1:
                    return min_value
            return min_value


    def max_function(working_board):
        max_value = -1
        # Ends recursion to go up the call stack
        if terminal(working_board):
            return utility(working_board)
        else:
            # Recurses back to opposite function for every possible move
            for action in actions(working_board):
                max_value = max(max_value, min_function(result(working_board, action)))
                # Short alpha-beta prune, to stop when reached highest value, saves recursion time
                if max_value == 1:
                    return max_value
            return max_value

    # Runs minimax algorithm for max player
    if player(board) == X:
        final_actions = []
        # Runs for every current action
        for action in actions(board):
            # Starts recursion to find value of the current action
            current_value = min_function(result(board, action))
            
            # Expedites recursion a little
            if current_value == 1:
                return action
            final_actions.append((current_value, action))

        final_index = final_actions.index(max(final_actions))
        return final_actions[final_index][1]

    # Runs minimax algorithm for min player
    elif player(board) == O:
        final_actions = []
        # Runs for every current action
        for action in actions(board):
            # Starts recursion to find value of the current action
            current_value = max_function(result(board, action))
            
            # Expedites recursion a little
            if current_value == -1:
                return action
            final_actions.append((current_value, action))
        
        final_index = final_actions.index(min(final_actions))
        return final_actions[final_index][1]
    


    