# Author: Josephine Lyou
# GitHub username: yuzuhaidan
# Date: 3/6/25
# Description: This file allows a game of Chess to be played that follows the King of the Hill variant rules.

class Player:
    """ Represents a player in chess. Used by ChessVar class. All data members are private. """
    def __init__(self, color):
        """ Takes color (white or black) as a string. Initializes the color. """
        self._color = color

    def get_color(self):
        """ Return's player's color."""
        return self._color

class ChessVar:
    """ Represents a Chess game that follows King of the Hill rules. All data members are private. Sets up the board, tracks the game state, tracks turns, board state, removed pieces, and an x-axis string for conversion """
    def __init__(self):
        """ Initialize two players, the game state, game board of nested lists. White always goes first. Tracks turn. Tracks board state with moves. Tracks removed pieces as game progresses. Initializes string of x-axis for conversion from algebraic notation to indices. """
        player_white = Player('white')
        player_black = Player('black')
        self._game_state = 'UNFINISHED' # 'WHITE_WON' or 'BLACK_WON'
        self._whose_turn = 'white'
        self._board = [ ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] ] #initialize the game board
        self._removed = [] # track removed pieces in a list
        self._x_axis_lookup = "abcdefgh"
        self._y_axis_lookup = "87654321"

    def get_game_state(self):
        """ Returns 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'. """
        return self._game_state

    def get_board(self):
        """ Returns the board's current state in a single line. """
        return self._board

    def get_turn(self):
        """ Returns the current player's turn. """
        return self._whose_turn

    def get_removed(self):
        """ Returns the removed pieces of the game so far. """
        return self._removed

    def write_to_board(self, first, second, board):
        """ Takes indices of first and second position of a piece and commits a valid make_move() to the board. Checks if a piece is eaten and places eaten piece in self._removed if so. Updates turn and returns True."""
        if board[second[0]][second[1]] != ' ': # if destination has piece
            self._removed.append(board[second[0]][second[1]]) # add eaten piece to removed list
        board[second[0]][second[1]] = board[first[0]][first[1]] # apply first to second
        board[first[0]][first[1]] = ' '  # erase original position
        ##########  CHECK IF SOMEONE WON
        # THE HILL
        if 'k' == board[3][3] or 'k' == board[4][3] or 'k' == board[3][4] or 'k' == board[4][4]:
            self._game_state = 'BLACK_WON'
        if 'K' == board[3][3] or 'K' == board[4][3] or 'K' == board[3][4] or 'K' == board[4][4]:
            self._game_state = 'WHITE_WON'
        # KING IS EATEN
        if 'k' in self._removed:
            self._game_state = 'WHITE_WON'
        if 'K' in self._removed:
            self._game_state = 'BLACK_WON'
        # change whose turn it is
        if self._whose_turn == 'white':
            self._whose_turn = 'black'
        else:
            self._whose_turn = 'white'
        return True # 'UNFINISHED', move completed, turn changed

    def pawn_move(self, first, second, board):
        """ Takes first and second positions as strings in index form from make_move(). Can move one or two spaces forward. Returns True if valid, otherwise False. Checks if blocked. Can never move backward. """
        step = 0
        if board[first[0]][first[1]].islower():
            step = 1
        else:
            step = -1

        # rule out columns less or greater than eating logic
        if first[1] - 1 > second[1] or first[1] + 1 < second[1]:
            return False
        # rule out rows greater than 2 steps
        if board[first[0]][first[1]].islower(): # if black piece
            if second[0] > first[0] + 2:
                return False # cannot be farther than 2 ahead
            if second[0] < first[0] + 1:
                return False # cannot be same place or behind
        if board[first[0]][first[1]].isupper(): # if white piece
            if second[0] < first[0] - 2:
                return False # cannot be farther than 2 ahead
            if second[0] > first[0] - 1:
                return False # cannot be same place or behind

        if second[0] == first[0] + step: # if desti is one move
            if second[1] == first[1]:
                return board[second[0]][second[1]] == ' ' # return False if block
            else: # diagonal, if eating
                return board[second[0]][second[1]] != ' ' # True if there's something to eat
        elif second[0] == first[0] + (2 * step): # if move two
            if board[first[0]][first[1]].islower() and first[0] != 1: # if black
                return False # pawn has moved before
            if board[first[0]][first[1]].isupper() and first[0] != 6: # if white
                return False
            # check if moving in same column and not blocked
            return second[1] == first[1] and board[second[0]][second[1]] == ' '
        return False

    def rook_move(self, first, second, board):
        """ Takes first and second positions as strings in index form from make_move(). Can move up or down any number within board boundaries, or left or right any number within board boundaries. Returns True if valid, else False. """
        ####### IF MOVING
        # VERTICAL HORIZONTAL
        if first[0] == second[0]: # IF X SAME, HORIZONTAL
            # CHECK IF BLOCKED
            if first[1] > second[1]:
                for num in range(second[1] + 1, first[1]):
                    if board[first[0]][num] != ' ':
                        if board[first[0]][num] != board[second[0]][second[1]]:
                            return False # go left, blocked
            elif first[1] < second[1]:
                for num in range(first[1] + 1, second[1]):
                    if board[first[0]][num] != ' ':
                        if board[first[0]][num] != board[second[0]][second[1]]:
                            return False # go right, blocked
            return True
        elif first[1] == second[1]: # IF Y SAME, VERTICAL
            # CHECK IF BLOCKED
            if first[0] > second[0]:
                for num in range(first[0] - 1, second[0], -1):
                    if board[num][first[1]] != ' ':
                        return False # go up, blocked
            if first[0] < second[0]:
                for num in range(second[0] - 1, first[0], -1):
                    if board[num][first[1]] != ' ':
                        return False # go down, blocked
            return True
        return False

    def knight_move(self, first, second):
        """ Takes first and second positions as strings representing index form from make_move(). Can move two squares up and one square right or left. Can jump, no blocking can happen. Returns True if valid, False otherwise. """
        #### MOVE UP
        if first[0] - 2 == second[0] and first[1] - 1 == second[1]:
            return True # up left, valid
        elif first[0] - 2 == second[0] and first[1] + 1 == second[1]:
            return True # up right, valid
        #### MOVE DOWN
        elif first[0] + 2 == second[0] and first[1] - 1 == second[1]:
            return True # down left, valid
        elif first[0] + 2 == second[0] and first[1] + 1 == second[1]:
            return True # down right, valid
        #### MOVE RIGHT
        elif first[0] - 1 == second[0] and first[1] + 2 == second[1]:
            return True # right up
        elif first[0] + 1 == second[0] and first[1] + 2 == second[1]:
            return True # right down
        #### MOVE LEFT
        elif first[0] - 1 == second[0] and first[1] - 2 == second[1]:
            return True # left up
        elif first[0] + 1 == second[0] and first[1] - 2 == second[1]:
            return True # left down
        return False

    def bishop_move(self, first, second, board):
        """ Takes first and second positions as strings representing index form from make_move(). Can move/down up one and right/left one square. Returns True if valid, False otherwise. """
        # DIAGONAL
        if abs(second[0] - first[0]) == abs(second[1] - first[1]):
            # CHECK IF BLOCKED
            ######### DOWN
            if first[0] < second[0] and first[1] > second[1]: # down left
                for num in range(1, abs(first[0] - second[0])):
                    if board[first[0] + num][first[1] - num] != ' ':
                        return False # blocked, invalid move
            if first[0] < second[0] and first[1] < second[1]: # down right
                for num in range(1, abs(first[0] - second[0])):
                    if board[first[0] + num][first[0] + num] != ' ':
                        return False # blocked, invalid move
            ######### UP
            if first[0] > second[0] and first[1] > second[1]: # up left
                for num in range(1, abs(first[0] - second[0])):
                    if board[first[0] - num][first[1] - num] != ' ':
                        return False # blocked, invalid move
            if first[0] > second[0] and second[1] > first[1]: # up right
                for num in range(1, abs(first[0] - second[0])):
                    if board[first[0] - num][first[1] + num] != ' ':
                        return False # blocked, invalid move
            return True
        return False

    def queen_move(self, first, second, board):
        """ Takes first and second positions as strings representing index form from make_move(). Can move like bishop and rook together. Returns True if valid, False otherwise."""
        if self.bishop_move(first, second, board):
            return True
        if self.rook_move(first, second, board):
            return True
        else:
            return False

    def king_move(self, first, second, board):
        """ Takes first and second positions as strings representing index form from make_move(). Can move one square up, down, left or right within board boundaries. Returns True if valid move, else False. """
        if first[0] - 1 == second[0] and first[1] == second[1]:
            return True # move up
        elif first[0] + 1 == second[0] and first[1] == second[1]:
            return True # move down
        elif first[0] == second[0] and first[1] - 1 == second[1]:
            return True # move left
        elif first[0] == second[0] and first[1] + 1 == second[1]:
            return True # move right
        elif first[0] + 1 == second[0] and first[1] - 1 == second[1]:
            return True # move down left
        elif first[0] + 1 == second[0] and first[1] + 1 == second[1]:
            return True # move down right
        elif first[0] - 1 == second[0] and first[1] - 1 == second[1]:
            return True # move up left
        elif first[0] - 1 == second[0] and first[1] + 1 == second[1]:
            return True # move up right
        else:
            return False

    def make_move(self, origin, destination):
        """ Takes strings that represent the square moved from and the square moved to. If empty first or illegal move, return False. Else call write_to_board() which does these things: update piece pos, delete captured piece and add it to removed list, check if needs update_game_state, update turn, and Return True. """
        if self._game_state !='UNFINISHED':
            return False
        if origin == destination:
            return False

        first = [0, 0]
        second = [0, 0]
        first[1] = self._x_axis_lookup.index(origin[0])  # change algebraic to index
        first[0] = self._y_axis_lookup.index(origin[1])
        second[1] = self._x_axis_lookup.index(destination[0])
        second[0] = self._y_axis_lookup.index(destination[1])

        # CHECK IF OUT OF BOUNDS
        if 0 > first[0] or first[0] > 7 or 0 > first[1] or first[1] > 7 or 0 > second[0] or second[0] > 7 or 0 > second[1] or second[1] > 7:
            return False
        if self._board[first[0]][first[1]].isupper() and self._whose_turn == 'black':
            return False
        if self._board[first[0]][first[1]].islower() and self._whose_turn == 'white':
            return False
        if self._board[first[0]][first[1]].isupper() and self._board[second[0]][second[1]].isupper():
            return False
        if self._board[first[0]][first[1]].islower() and self._board[second[0]][second[1]].islower():
            return False
        else:
            if self._board[first[0]][first[1]] == ' ': # if empty
                return False
            elif self._board[first[0]][first[1]] == 'p' or self._board[first[0]][first[1]] == 'P':
                if self.pawn_move(first, second, self._board): # move valid
                    return self.write_to_board(first, second, self._board)
            elif self._board[first[0]][first[1]] == 'r' or self._board[first[0]][first[1]] == 'R':
                if self.rook_move(first, second, self._board):
                    return self.write_to_board(first, second, self._board)
            elif self._board[first[0]][first[1]] == 'n' or self._board[first[0]][first[1]] == 'N':
                if self.knight_move(first, second):
                    return self.write_to_board(first, second, self._board)
            elif self._board[first[0]][first[1]] == 'b' or self._board[first[0]][first[1]] == 'B':
                if self.bishop_move(first, second, self._board):
                    return self.write_to_board(first, second, self._board)
            elif self._board[first[0]][first[1]] == 'q' or self._board[first[0]][first[1]] == 'Q':
                if self.queen_move(first, second, self._board):
                    return self.write_to_board(first, second, self._board)
            elif self._board[first[0]][first[1]] == 'k' or self._board[first[0]][first[1]] == 'K':
                if self.king_move(first, second, self._board):
                    return self.write_to_board(first, second, self._board)
            else: # if move is False
                return False
        return False

