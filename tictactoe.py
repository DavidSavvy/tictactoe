"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
from pickle import NONE
import random

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
    - Might be problematic with the way the winner is decided using the current player(board), keep in mind
    """
    current_player = None
    if player(board) == X:
        current_player = O
    else:
        current_player = X
    
    for i in range(0,3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY or board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return current_player
    
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
    """
    works a little better, not always the best move 
    """
    #print(actions(board))
    if terminal(board):
        return None
    #global current_min
    #current_min = 1
    def min_function(working_board):
        final_action = None
        current_min = 1
        is_finished = False
        #global current_min
        if terminal(working_board):
            #print("min done")
            #print(utility(working_board))
            #print(working_board)
            is_finished = True
            return (utility(working_board), None)
        else:
            
            for action in actions(working_board):
                #print('minstart',working_board)
                #print(actions(working_board))
                print("min run")
                function_value = max_function(result(working_board, action))[0]
                """
                if working_board is not board:
                    return (function_value, None)
                elif working_board is board:
                    if function_value < current_min:
                        current_min = function_value
                        final_action = action
                    print("done")
                """
                
                if function_value < current_min and working_board == board:
                    current_min = function_value
                    final_action = action
                
                #print('minend',working_board)
                #print(current_min)
            return (current_min, final_action)
    #global current_max
    #current_max = -1        
    def max_function(working_board):
        #print(working_board)
        #global current_max
        
        is_finished = False
        if terminal(working_board):
            #print("max done")
            #print(utility(working_board))
            is_finished = True
            return (utility(working_board), None)
        else:
            
            for action in actions(working_board):
                #print('maxstart',working_board)
                #print(actions(working_board))
                final_action = None
                current_max = -1
                print("max run")
                function_value = min_function(result(working_board, action))[0]
                
                """
                if working_board is not board and is_finished:
                    return (function_value, None)
                elif working_board is board:
                    if function_value > current_max:
                        current_max = function_value
                        final_action = action
                    print("done")
                """
                if function_value > current_max:
                    current_max = function_value
                    final_action = action
                #print('maxend',working_board)
                #print(current_max)
            return (current_max, final_action)

    outer_final_action = None
    if player(board) == X:
        #final_max = -1 
        

        outer_final_action = max_function(board)[1]
        

        """
        for action in actions(board):
            new_board = result(board, action)
            predicted_max = min_function(new_board)
            if predicted_max > final_max:
                final_action = action
            print(action)
        #print(final_action)
        if final_action == None:
            #print(random.choice(list(actions(board))))
            final_action = random.choice(list(actions(board)))
        """
    else:
        #final_min = 1
        
        outer_final_action = min_function(board)[1]
        """
        for action in actions(board):
            new_board = result(board, action)
            predicted_min = max_function(new_board)
            if predicted_min < final_min:
                final_action = action
            print(action)
        #print(final_action)
        if final_action == None:
            final_action = random.choice(list(actions(board)))
            #print(random.choice(list(actions(board))))
        """
    if outer_final_action == None:
        outer_final_action = random.choice(list(actions(board)))
    print(outer_final_action)
    return outer_final_action
    


    """
    Traceback (most recent call last):
        File "T:\tictactoe\runner.py", line 116, in <module>
            board = ttt.result(board, move)
                    ^^^^^^^^^^^^^^^^^^^^^^^
        File "T:\tictactoe\tictactoe.py", line 54, in result
            if board_copy[action[0]][action[1]] == EMPTY:
                        ~~~~~~^^^
    TypeError: 'NoneType' object is not subscriptable

    minimax() function seems to not return a real final_action in very specfic moves
    might have to do with winner function? seems to have to do with the center square
    """