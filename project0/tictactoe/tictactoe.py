"""
Tic Tac Toe Player
"""

import math, copy, random

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

    # initializa variables to hold count of X and O moves
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
    # create the variable that holds the return value
    actions = set()

    # iterate trough all cells and add them to the possible actions
    # if they are EMPTY
    for x in range(3):
        for y in range(3):
            if board[x][y] == EMPTY:
                actions.add((x,y))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # raise exception if action is None
    if action == None:
        raise Exception('There are no possible actions')
    
    # raise exception if action is out of bounds
    if action[0] < 0 or action[1] < 0 or action[0] > 2 or action[1] > 2:
        raise Exception('Action out of bounds')
    
    # raise exception if action points to a 'busy' cell
    if board[action[0]][action[1]] is not None:
        raise Exception('Can not overwrite this cell')
    
    # create a deepcopy of the board
    updated_board = copy.deepcopy(board)

    # get the next player to move and change the cell in the copy
    updated_board[action[0]][action[1]] = player(board)

    # return the updated board
    return updated_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    has_a_line = None
    # iterate trough x,y in the board
    for x in range(3):
        for y in range(3):

            # check first diagonal
            if x == 1 and y == 1:
                has_a_line = board[x][y] if board[x-1][y-1] == board[x][y] == board[x+1][y+1] else None

                # check second diagonal if no winner was found
                if has_a_line == None:
                    has_a_line = board[x][y] if board[x+1][y-1] == board[x][y] == board[x-1][y+1] else None

            # check horizontal lines
            if x == 1 and has_a_line == None:
                has_a_line = board[x][y] if board[x-1][y] == board[x][y] == board[x+1][y] else None

            # check vertical lines
            if y == 1 and has_a_line == None:
                has_a_line = board[x][y] if board[x][y-1] == board[x][y] == board[x][y+1] else None

            # return a winner if one is found
            if has_a_line:
                return has_a_line
            
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

    # iterate trough all positions in all lines and 
    # return false if there is still empty positions
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
            
    # If there is no winner, and all positions are occupied return True(Game Over)
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # returns 0 if there are no winners
    if winner(board) == None:
        return 0
    # return 1 if X wins
    elif winner(board) == X:
        return 1
    # or -1 if O wins
    else:
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # return none if the game has ended
    if terminal(board):
        return None
    
    # bool variable to store who's turn it is
    is_max_player = player(board) == X

    # initialize a moves dictionary, that will store all possible actions and their value
    moves_dict = {}

    # iterate trough every possible action and call get_move_utility
    for action in actions(board):
        moves_dict[action] = get_move_utility(result(board, action), not is_max_player)

    # initialize the target value for the minimax loop - oposite to target
    target_value = -math.inf if is_max_player else math.inf

    # set target_value to be the best value the player can reach
    for val in moves_dict.values():
        target_value = max(target_value, val) if is_max_player else min(target_value, val)

    # filter out the keys that cant reach optimal results
    matching_keys = [k for k, v in moves_dict.items() if v == target_value]

    # added some variation when picking from the best possible moves
    return random.choice(matching_keys)


# get the utility for each possible move
def get_move_utility(state, is_max_player):

    # return utility if state is terminal
    if terminal(state):
        return utility(state)

    # initialize value to positive or negative infinity
    value = -math.inf if is_max_player else math.inf

    # iterate recursively trough every possible action for a given state
    for action in actions(state):

        # recursive function call, inverting is_max_player
        child_value = get_move_utility(result(state, action), not is_max_player)

        # keep track of the best result
        value = max(value, child_value) if is_max_player else min(value, child_value)

    # return the value for the given state
    return value
