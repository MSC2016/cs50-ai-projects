"""
Tic Tac Toe Player
"""

import math

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

    #initializa variables to count the amount of moves each player has done
    x_count = 0
    o_count = 0

    # iterate trough the board and count the amount of X and O moves
    for x in range(3):
        for y in range(3):
            if board[x][y] == X:
                x_count += 1
            if board[x][y] == O:
                o_count += 1
    
    # return O if X has done more moves
    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    winner = None
    # iterate trough x,y in the board
    for x in range(3):
        for y in range(3):

            # check first diagonal
            if x == 1 and y == 1:
                winner = board[x][y] if board[x-1][y-1] == board[x][y] == board[x+1][y+1] else None

                # check second diagonal if no winner was found
                if winner == None:
                    winner = board[x][y] if board[x+1][y-1] == board[x][y] == board[x-1][y+1] else None

            # check horizontal lines
            if x == 1 and winner == None:
                winner = board[x][y] if board[x-1][y] == board[x][y] == board[x+1][y] else None

            # check vertical lines
            if y == 1 and winner == None:
                winner = board[x][y] if board[x][y-1] == board[x][y] == board[x][y+1] else None

            # return a winner if one is found
            if winner:
                return winner
            
            # previous if statements checked if a winner was found before to avoid
            # overwritting a previously found winning line, with a line of EMPTY cells 

    # return None if no winner was found        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if one of the players has won, return true (Game Over)
    if winner(board) != None:
        return True

    #iterate trough all positions in all lines and 
    # return false if there is still empty positions
    for line in board:
        for position in line:
            if position == EMPTY:
                return False
            
    #If there is no winner, and all positions are occupied return True(Game Over)
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
