# Author: Bryan Zierk
# Date: 2/26/21
# Description: This program allows the user to play Janggi, a Korean board game similar to Xiangqi or Chinese Chess.
# The game is played on a board which is 9 lines wide by 10 lines tall where pieces are placed at the intersection
# of lines similar to Go. Players take turns moving pieces in an attempt to trap the opposing player's General. A player
# is victorious once they have checkmated the opposing general by leaving them no remaining valid moves.

import string

class JanggiGame:
    def __init__(self):
        """
        Builds the Janggi board. A rectangular board with lines creating 90 intersections in a 9x10 grid on which
        pieces can be placed.
        """
        self._active_turn = 'b'
        self._board = [
            [Chariot('r', 0, 0), Elephant('r', 0, 1), Horse('r', 0, 2), Guard('r', 0, 3), None, Guard('r', 0, 5),
             Elephant('r', 0, 6), Horse('r', 0, 7), Chariot('r', 0, 8)],
            [None, None, None, None, General('r', 1, 4), None, None, None, None],
            [None, Cannon('r', 2, 1), None, None, None, None, None, Cannon('r', 2, 7), None],
            [Soldier('r', 3, 0), None, Soldier('r', 3, 2), None, Soldier('r', 3, 4), None, Soldier('r', 3, 6), None,
             Soldier('r', 3, 8)],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [Soldier('b', 6, 0), None, Soldier('b', 6, 2), None, Soldier('b', 6, 4), None, Soldier('b', 6, 6), None,
             Soldier('b', 6, 8)],
            [None, Cannon('b', 7, 1), None, None, None, None, None, Cannon('b', 7, 7), None],
            [None, None, None, None, General('b', 8, 4), None, None, None, None],
            [Chariot('b', 9, 0), Elephant('b', 9, 1), Horse('b', 9, 2), Guard('b', 9, 3), None, Guard('b', 9, 5),
             Elephant('b', 9, 6), Horse('b', 9, 7), Chariot('b', 9, 8)],
        ]
        self._game_state = 'UNFINISHED'

    def get_board(self):
        """
        Returns a list of lists which represent the current board setup
        """
        return self._board

    def terminal_print_board(self):
        """
        Prints a semi-readable version of the board in case you aren't using the GUI. Primarily for debugging purposes
        """
        print('-----------------------------------------------------------')
        for row in range(len(self._board)):
            for column in range(len(self._board[row])):
                if self._board[row][column] is not None:
                    print(self._board[row][column].get_name(), end=" ")
                else:
                    print('--', end=" ")
            print()
        print('-----------------------------------------------------------')

    def active_turn(self):
        """
        If it is blue's turn, returns 'b', if red, returns 'r'.
        """
        return self._active_turn

    def set_next_turn(self):
        """
        If blue_to_play is True, sets it to False, otherwise sets to True.
        """
        if self._active_turn == 'b':
            self._active_turn = 'r'
        else:
            self._active_turn = 'b'

    def get_game_state(self):
        """
        Returns the current game state
        """
        return self._game_state

    def set_game_state(self, new_gs):
        """
        Takes 'UNFINISHED', 'RED WON', or 'BLUE WON' as a parameter and updates the game state
        """
        self._game_state = new_gs

    def is_in_check(self, color):
        """
        Takes 'red' or 'blue' as a parameter and checks if that color's General is in check. Returns True if the
        general is in check, otherwise returns False
        """
        pass

    @staticmethod
    def letter_to_number(char):
        """
        Takes a single letter as a parameter and returns the equivalent index number. Used to convert column letter
        identifiers into an iterable numeric value.
        """
        return string.ascii_lowercase.index(char.lower())

    def validate_move(self, orig, dest, piece):
        """
        Takes two strings as parameters which represent the origin square and destination square. Validates the move
        and returns True if the move is allowed, otherwise returns False.
        """
        # verify game state
        if self._game_state != 'UNFINISHED':
            return False

        # test that selected squares are in range (on the board)
        squares = [orig, dest]
        for square in squares:
            if square[0] > 'i':
                return False

            if int(square[1:]) > 10 or int(square[1:]) < 1:
                return False

        # check that the player is moving their own piece
        if piece.get_color() != self._active_turn:
            return False

        return True
        # test that the move is allowed for the selected piece

    def make_move(self, orig, dest):
        """
        Takes two strings as parameters which represent the square which a piece is moving from and moving to. The
        squares should be identified using algebraic notation with columns labeled a-i and rows labeled 1-10 where
        row 1 is the Red side and row 10 is the Blue side.
        """
        # grabs piece to be moved
        orig_piece = self._board[int(orig[1:]) - 1][int(self.letter_to_number(orig[0]))]

        # validate move
        if not self.validate_move(orig, dest, orig_piece):
            return False

        # get valid moves
        moves = set()
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                if self._board[row][col] is not None:
                    self._board[row][col].get_legal_moves(self._board, moves)

        # allow player to pass
        if orig == dest:
            self.set_next_turn()
            return True

        # store destination piece in case move is invalid and needs to be reverted
        dest_piece = self._board[int(dest[1:])-1][int(self.letter_to_number(dest[0]))]

        print(orig_piece.get_row(), orig_piece.get_col())
        orig_piece.set_col(int(self.letter_to_number(dest[0])))
        orig_piece.set_row(int(dest[1:])-1)
        print(orig_piece.get_row(), orig_piece.get_col())
        self._board[int(orig[1:]) - 1][int(self.letter_to_number(orig[0]))] = None
        self._board[int(dest[1:]) - 1][int(self.letter_to_number(dest[0]))] = orig_piece
        self.set_next_turn()

    def make_move_helper(self, move):
        """
        Helper function to move pieces and update the board.
        """


    def fill_possible_moves(self):
        """
        This function generates all possible moves for a player, regardless of whether or not the move would leave
        that player's general in check.
        """
        possible_moves = []
        for r in range(len(self._board)):
            for c in range(len(self._board[r])):
                if self._board[r][c].get_color() == self._active_turn:
                    sel_piece = self._board[r][c].get_name()
                    if sel_piece == "Cannon":
                        self.cannonMoves()
                    elif sel_piece == "Chariot":
                        self.chariotMoves()
                    elif sel_piece == "Elephant":
                        self.elephantMoves()
                    elif sel_piece == "General":
                        self.generalMoves()
                    elif sel_piece == "Guard":
                        self.guardMoves()
                    elif sel_piece == "Horse":
                        self.horseMoves()
                    elif sel_piece == "Soldier":
                        self.soldierMoves()

    def get_valid_moves(self):
        pass



class Piece:
    """
    This class will contain be the super class for each individual Janggi piece. Each piece object will contain
    information about their color and their position on the board, they will inherit this class and have piece
    specific move validation.
    """
    def __init__(self, color, row, col):
        self._color = color
        self._col = col
        self._row = row
        #self._board = JanggiGame()

    def get_color(self):
        """
        Returns the color of a piece
        """
        return self._color

    def get_col(self):
        """
        Returns the current column value of a piece
        """
        return self._col

    def get_row(self):
        """
        Returns the current row value of a piece
        """
        return self._row

    def set_col(self, new_col):
        """
        Updates the column value of a piece
        """
        self._col = new_col

    def set_row(self, new_row):
        """
        Updates the row value of a piece
        """
        self._row = new_row

    def gen_move_id(self, new_row, new_col):
        """
        Converts position coordinates into a concatenated string which will be used as a unique move identifier for
        storing valid moves (ie 0111 represents a piece moving from a2 to b2)
        """
        return self._row * 1000 + self._col * 100 + new_row * 10 + new_col

class Cannon(Piece):
    """
    Creates a Cannon object which contains color, position, and valid move information.
    """
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._name = 'Cannon'

    def get_name(self):
        return self._name

    def get_legal_moves(self, board, moves):
        """
        Generates a set of all legal moves for the piece given the current board condition. Does not account for
        check, so not all legal moves are valid.
        """
        pass
class Chariot(Piece):
    """
    Creates a Chariot object which contains color, position, and valid move information.
    """
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._name = 'Chariot'

    def get_name(self):
        return self._name

    def get_legal_moves(self, board, moves):
        """
        Generates a set of all legal moves for the piece given the current board condition. Does not account for
        check, so not all legal moves are valid.
        """
        pass

class Elephant(Piece):
    """
    Creates a Elephant object which contains color, position, and valid move information.
    """

    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._name = 'Elephant'

    def get_name(self):
        return self._name

    def get_legal_moves(self, board, moves):
        """
        Generates a set of all legal moves for the piece given the current board condition. Does not account for
        check, so not all legal moves are valid.
        """
        pass

class General(Piece):
    """
    Creates a General object which contains color, position, and valid move information.
    """

    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._name = 'General'

    def get_name(self):
        return self._name

    def get_legal_moves(self, board, moves):
        """
        Generates a set of all legal moves for the piece given the current board condition. Does not account for
        check, so not all legal moves are valid.
        """
        pass

class Guard(Piece):
    """
    Creates a Guard object which contains color, position, and valid move information.
    """

    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._name = 'Guard'

    def get_name(self):
        return self._name

    def get_legal_moves(self, board, moves):
        """
        Generates a set of all legal moves for the piece given the current board condition. Does not account for
        check, so not all legal moves are valid.
        """
        pass

class Horse(Piece):
    """
    Creates a Horse object which contains color, position, and valid move information.
    """

    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._name = 'Horse'

    def get_name(self):
        return self._name

    def get_legal_moves(self, board, moves):
        """
        Generates a set of all legal moves for the piece given the current board condition. Does not account for
        check, so not all legal moves are valid.
        """
        pass

class Soldier(Piece):
    """
    Creates a Soldier object which contains color, position, and valid move information.
    """

    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self._name = 'Soldier'

    def get_name(self):
        return self._name

    def get_legal_moves(self, board, moves):
        """
        Generates a set of all legal moves for the piece given the current board condition. Does not account for
        check, so not all legal moves are valid.
        """
        #moves = set()

        dir = {'r': 1, 'b': -1}
        poss_moves = ((0, -1), (0, 1), (dir[self._color], 0))

        for row, col in poss_moves:
            new_row, new_col = self._row + row, self._col + col
            if 0 <= new_row <= 9 and 0 <= new_col <= 8:
                if board[new_row][new_col] is None:
                    moves.add(self.gen_move_id(new_row, new_col))
        print(moves)
        return moves


class Move:
    """
    Still considering this. Would allow for easier tracking of past moves.
    """
    def __init__(self, orig, dest, cur_board):
        self._orig_row = int(orig[1:])
        self._orig_col = int(self.letter_to_number(orig[0]))
        self._dest_row = int(dest[1:])
        self._dest_col = int(self.letter_to_number(dest[0]))
        self._piece = cur_board[self._orig_row][self._orig_col]
        self._target = cur_board[self._dest_row][self._dest_col]
        self._cur_board = cur_board

    @staticmethod
    def letter_to_number(char):
        """
        Takes a single letter as a parameter and returns the equivalent index number. Used to convert column letter
        identifiers into an iterable numeric value.
        """
        return string.ascii_lowercase.index(char.lower())



gs = JanggiGame()

#print(gs.terminal_print_board())
gs.make_move('a7', 'a6')
#print(gs.terminal_print_board())
#print(gs.get_board()[1][0].get_name())
#gs.fillPossibleMoves()
#print(gs.get_board())
