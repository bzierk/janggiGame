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
        return self._board.copy()

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

    def make_move(self, orig, dest):
        """
        Takes two strings as parameters which represent the square which a piece is moving from and moving to. The
        squares should be identified using algebraic notation with columns labeled a-i and rows labeled 1-10 where
        row 1 is the Red side and row 10 is the Blue side.
        """
        if self._game_state != 'UNFINISHED':
            return False

        orig_pair = (int(orig[1:]) - 1, int(self.letter_to_number(orig[0])))
        dest_pair = (int(dest[1:]) - 1, int(self.letter_to_number(dest[0])))
        move = Move(orig_pair, dest_pair, self._board)
        self.make_move_helper(move)

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
        """

    def make_move_helper(self, move):
        """
        Helper function to move pieces and update the board.
        """

        orig_piece = move.get_original_piece()
        self._board[move.get_orig()[0]][move.get_orig()[1]] = None
        self._board[move.get_target()[0]][move.get_target()[1]] = orig_piece
        orig_piece.set_row(move.get_target()[0])
        orig_piece.set_col(move.get_target()[1])
        self.set_next_turn()

    def fill_possible_moves(self):
        """
        This function generates all possible moves for a player, regardless of whether or not the move would leave
        that player's general in check.
        """
        valid_moves = []
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                if self._board[row][col] is not None:
                    if self._board[row][col].get_color() == self._active_turn:
                        self._board[row][col].get_legal_moves(self._board, valid_moves)
                        """
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
                        """

        return valid_moves

    def get_valid_moves(self):
        return self.fill_possible_moves()




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

    def get_orig(self):
        return self._row, self._col

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

    def valid_space_check(self, row, col, board, my_color):
        """
        Generic function which checks that a target square can be occupied. Takes a target row, column, board instance,
        and moving piece's color as parameters. If the target space is on the board and either empty
        or occupied by a piece of the other color, returns True, otherwise if it is occupied by a piece of the
        same color, returns False.
        """
        if row < 0 or row > 9 or col < 0 or col > 8:
            return False
        if board[row][col] is None:
            return True
        elif board[row][col].get_color() != my_color:
            return True
        else:
            return False

    def red_palace_check(self, row, col, board, my_color):
        """
        Generic function which checks that a target palace square can be occupied. Takes a target row, column, board
        instance,and moving piece's color as parameters. If the target space is on the board and either empty
        or occupied by a piece of the other color, returns True, otherwise if it is occupied by a piece of the
        same color, returns False.
        """
        if row < 0 or row > 2 or col < 3 or col > 5:
            return False
        if board[row][col] is None:
            return True
        elif board[row][col].get_color() != my_color:
            return True
        else:
            return False

    def blue_palace_check(self, row, col, board, my_color):
        """
        Generic function which checks that a target palace square can be occupied. Takes a target row, column, board
        instance,and moving piece's color as parameters. If the target space is on the board and either empty
        or occupied by a piece of the other color, returns True, otherwise if it is occupied by a piece of the
        same color, returns False.
        """
        if row < 7 or row > 9 or col < 3 or col > 5:
            return False
        if board[row][col] is None:
            return True
        elif board[row][col].get_color() != my_color:
            return True
        else:
            return False


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
        poss_moves = ((-1, 0), (1, 0), (0, -1), (0, 1))

        for row, col in poss_moves:
            new_row, new_col = self._row + row, self._col + col
            while self.valid_space_check(new_row, new_col, board, self._color):
                moves.append(Move((self._row, self._col), (new_row, new_col), board))
                # Piece cannot go through multiple opponents. If opponent is found in one direction, stop looking.
                if board[new_row][new_col] is not None and board[new_row][new_col].get_color() != self._color:
                    break
                new_row += row
                new_col += col


        blue_palace = [(9, 3), (9, 5), (7, 3), (7, 5), (8, 4)]
        red_palace = [(0, 3), (0, 5), (2, 3), (2, 5), (1, 4)]
        palace_moves = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        if self.get_orig() in red_palace:
            for row, col in palace_moves:
                new_row, new_col = self._row + row, self._col + col
                while self.red_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))
                    if board[new_row][new_col] is not None and board[new_row][new_col].get_color() != self._color:
                        break
                    new_row += row
                    new_col += col

        if self.get_orig() in blue_palace:
            for row, col in palace_moves:
                new_row, new_col = self._row + row, self._col + col
                while self.blue_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))
                    if board[new_row][new_col] is not None and board[new_row][new_col].get_color() != self._color:
                        break
                    new_row += row
                    new_col += col


        """
        if self._row == 1 and self._col == 4:
            for row, col in red_palace:
                if self.valid_space_check(row, col, board, self._color):
                    moves.append(Move((self._row, self._col), (row, col), board))

        if self._row == 8 and self._col == 4:
            for row, col in blue_palace:
                if self.valid_space_check(row, col, board, self._color):
                    moves.append(Move((self._row, self._col), (row, col), board))

        if self._row == 2 or self._row == 0:
            if self._col == 3 or self._col == 5:
                if board[1][4] is None or board[1][4].get_color() != self._color:
                    moves.append(Move((self._row, self._col), (1, 4), board))

        if self._row == 7 or self._row == 9:
            if self._col == 3 or self._col == 5:
                if board[8][4] is None or board[8][4].get_color() != self._color:
                    moves.append(Move((self._row, self._col), (8, 4), board))
        """


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

        dir = {'r': 1, 'b': -1}
        poss_moves = ((0, -1), (0, 1), (dir[self._color], 0))

        for row, col in poss_moves:
            new_row, new_col = self._row + row, self._col + col
            if self.valid_space_check(new_row, new_col, board, self._color):
                moves.append(Move((self._row, self._col), (new_row, new_col), board))

        blue_palace = [(9, 3), (9, 5)]
        red_palace = [(0, 3), (0, 5)]
        if self._row == 1 and self._col == 4:
            for row, col in red_palace:
                if self.valid_space_check(row, col, board, self._color):
                    moves.append(Move((self._row, self._col), (row, col), board))

        if self._row == 8 and self._col == 4:
            for row, col in blue_palace:
                if self.valid_space_check(row, col, board, self._color):
                    moves.append(Move((self._row, self._col), (row, col), board))

        if self._row == 2:
            if self._col == 3 or self._col == 5:
                if board[1][4] is None or board[1][4].get_color() != self._color:
                    moves.append(Move((self._row, self._col), (1, 4), board))

        if self._row == 7:
            if self._col == 3 or self._col == 5:
                if board[8][4] is None or board[8][4].get_color() != self._color:
                    moves.append(Move((self._row, self._col), (8, 4), board))

        return moves


class Move:
    """
    Still considering this. Would allow for easier tracking of past moves.
    """
    def __init__(self, orig, dest, cur_board):
        self._orig_row = orig[0]
        self._orig_col = orig[1]
        self._dest_row = dest[0]
        self._dest_col = dest[1]
        self._piece = cur_board[self._orig_row][self._orig_col]
        self._target = cur_board[self._dest_row][self._dest_col]
        self._cur_board = cur_board

        # Delete this when not using GUI
        self._moveID = self._orig_row * 1000 + self._orig_col * 100 + self._dest_row * 10 + self._dest_col

    def get_orig(self):
        """
        Returns the origin coordinates of a desired move
        """
        return self._orig_row, self._orig_col

    def get_target(self):
        """
        Returns the target of a move
        """
        return self._dest_row, self._dest_col

    def get_original_piece(self):
        """
        Returns the piece which is being moved
        """
        return self._piece

    def get_target_piece(self):
        """
        Returns the piece which was on the target space. This can be used to reset the move if a covered check is
        discovered
        """
        return self._target

    @staticmethod
    def letter_to_number(char):
        """
        Takes a single letter as a parameter and returns the equivalent index number. Used to convert column letter
        identifiers into an iterable numeric value.
        """
        return string.ascii_lowercase.index(char.lower())


    # Delete this when not using GUI
    def __eq__(self, other):
        if isinstance(other, Move):
            return self._moveID == other._moveID
        return False




gs = JanggiGame()
#print(gs.terminal_print_board())
#gs.make_move('a1', 'a2')
#test_move = Move((0, 0), (1, 0), gs.get_board())
#gs.make_move_helper(test_move)
#print(gs.terminal_print_board())
#gs.make_move('a7', 'a6')
#print(gs.terminal_print_board())
print(gs.get_board()[0][0].get_color())
#gs.fillPossibleMoves()
#print(gs.get_board())
