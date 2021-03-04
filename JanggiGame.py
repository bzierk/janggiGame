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
        pieces can be placed. This class receives information from the Piece class and its subclasses in order to
        populate the board and keep track of the type of piece, its color, and its current position.
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
        Used to change the active player. If it is currently blue's turn, 'b' will be changed to 'r', and vice versa.
        """
        if self._active_turn == 'b':
            self._active_turn = 'r'
        else:
            self._active_turn = 'b'

    def get_game_state(self):
        """
        Returns the current game state ('UNFINISHED', 'RED_WON', or 'BLUE_WON')
        """
        return self._game_state

    def set_game_state(self, new_gs):
        """
        Takes a string, 'UNFINISHED', 'RED WON', or 'BLUE WON' as a parameter and updates the game state
        """
        self._game_state = new_gs

    def is_in_check(self, color):
        """
        Takes 'red' or 'blue' as a parameter and iterates through the board to locate the general of that color.
        It takes this position and compares it against the possible moves of the other player. If the opponent has a
        valid move which ends on the General's current square, this function returns True. If there are no valid
        moves which would attack the specified general, the function returns False.
        """
        colors = {'red': 'r', 'blue': 'b'}
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                if self._board[row][col] is not None:
                    if self._board[row][col].get_name() == 'General':
                        if self._board[row][col].get_color() == colors[color]:
                            general_pos = self._board[row][col].get_orig()

        print(general_pos)



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
        row 1 is the Red side and row 10 is the Blue side. The move is then validated by verifying that the player
        is attempting to move a piece which belongs to them, the move follows the movement rules of the specified
        piece, and the move does not leave the attacking player's General in check. If the move is valid, the board
        is updated, the active turn is changed, if necessary the game state is updated, and the function returns True.
        Otherwise, if any of these conditions are not met, the function returns False.
        """
        orig_pair = (int(orig[1:]) - 1, int(self.letter_to_number(orig[0])))
        dest_pair = (int(dest[1:]) - 1, int(self.letter_to_number(dest[0])))

        if self._board[orig_pair[0]][orig_pair[1]] is None:
            return False

        if self._board[orig_pair[0]][orig_pair[1]].get_color() != self._active_turn:
            return False

        move = Move(orig_pair, dest_pair, self._board)

        if move not in self.get_valid_moves():
            return False

        if move.get_orig() == move.get_target():
            if not self.is_in_check(self._active_turn):
                self.set_next_turn()
                return True

        self.make_move_helper(move)
        self.set_next_turn()
        return self.make_move_helper(move)

    def make_move_helper(self, move):
        """
        Helper function which takes a Move class object as a parameter and uses the information within the object
        to update the board and update the information within the appropriate Piece class objects.
        """
        if self._game_state != 'UNFINISHED':
            return False

        orig_piece = move.get_original_piece()
        self._board[move.get_orig()[0]][move.get_orig()[1]] = None
        self._board[move.get_target()[0]][move.get_target()[1]] = orig_piece
        orig_piece.set_row(move.get_target()[0])
        orig_piece.set_col(move.get_target()[1])
        self.set_next_turn()
        return True

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

        return valid_moves

    def get_valid_moves(self):
        return self.fill_possible_moves()


class Piece:
    """
    This class serves as the super class for each individual Janggi piece. Each piece object will contain
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
        storing valid moves (ie 0111 represents a piece moving from a2 to b2) and will be passed to the __eq__ function
        for use in equating Move objects generated by the user and Move objects generated by the possible move
        functions.
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

    def is_in_palace(self, row, col):
        """
        If a coordinate is in the palace, returns True, if coordinate is outside of the palace, returns False.
        """
        if (9 >= row >= 7) or (2 >= row >= 0):
            if 5 >= col >= 3:
                return True

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
        # Allow player to pass
        moves.append(Move((self._row, self._col), (self._row, self._col), board))

        poss_moves = ((-1, 0), (1, 0), (0, -1), (0, 1))

        for row, col in poss_moves:
            can_jump = False
            new_row, new_col = self._row + row, self._col + col
            while 0 <= new_row <= 9 and 0 <= new_col <= 8:
                if not can_jump:
                    if board[new_row][new_col] is None:
                        new_row += row
                        new_col += col
                        continue
                    elif board[new_row][new_col].get_name() == 'Cannon':
                        break
                    else:
                        can_jump = True
                        new_row += row
                        new_col += col
                else:
                    if board[new_row][new_col] is None:
                        moves.append(Move((self._row, self._col), (new_row, new_col), board))
                        new_row += row
                        new_col += col
                    elif board[new_row][new_col].get_name() != 'Cannon' and board[new_row][new_col].get_color() !=\
                            self._color:
                        moves.append(Move((self._row, self._col), (new_row, new_col), board))
                        break
                    else:
                        break

        palace_squares = [(0, 3), (0, 5), (2, 3), (2, 5), (1, 4), (9, 3), (9, 5), (7, 3), (7, 5), (8, 4)]
        palace_moves = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

        # handles diagonal jumps in the palace
        if self.get_orig() in palace_squares:
            for row, col in palace_moves:
                new_row, new_col = self._row + row, self._col + col
                while self.is_in_palace(new_row, new_col):
                    if board[new_row][new_col] is None:
                        break
                    else:
                        if board[new_row][new_col].get_name() != 'Cannon':
                            new_row += row
                            new_col += col
                            if board[new_row][new_col] is None:
                                moves.append(Move((self._row, self._col), (new_row, new_col), board))
                            elif board[new_row][new_col].get_color() != self._color and \
                                    board[new_row][new_col].get_name() != 'Cannon':
                                moves.append(Move((self._row, self._col), (new_row, new_col), board))
                                break


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
        # Allow player to pass
        moves.append(Move((self._row, self._col), (self._row, self._col), board))

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
        # handles diagonal moves if chariot is in the red palace
        if self.get_orig() in red_palace:
            for row, col in palace_moves:
                new_row, new_col = self._row + row, self._col + col
                while self.red_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))
                    if board[new_row][new_col] is not None and board[new_row][new_col].get_color() != self._color:
                        break
                    new_row += row
                    new_col += col

        # handles diagonal moves if chariot is in the blue palace
        if self.get_orig() in blue_palace:
            for row, col in palace_moves:
                new_row, new_col = self._row + row, self._col + col
                while self.blue_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))
                    if board[new_row][new_col] is not None and board[new_row][new_col].get_color() != self._color:
                        break
                    new_row += row
                    new_col += col


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
        # Allow player to pass
        moves.append(Move((self._row, self._col), (self._row, self._col), board))

        poss_moves = ((-1, 0), (1, 0), (0, -1), (0, 1))
        directions = [-1, 1]

        for row, col in poss_moves:
            new_row, new_col = self._row + row, self._col + col
            if 0 < new_row < 9 and 0 < new_col < 8:
                if board[new_row][new_col] is None:
                    new_row += row
                    new_col += col
                    temp_coords = [new_row, new_col]
                    if row == 0:
                        for direction in directions:
                            new_col = temp_coords[1]
                            new_row = self._row + direction
                            if board[new_row][new_col] is None:
                                new_row += direction
                                new_col = new_col + col
                                if self.valid_space_check(new_row, new_col, board, self._color):
                                    moves.append(Move((self._row, self._col), (new_row, new_col), board))

                    if col == 0:
                        for direction in directions:
                            new_row = temp_coords[0]
                            new_col = self._col + direction
                            if board[new_row][new_col] is None:
                                new_row = new_row + row
                                new_col += direction
                                if self.valid_space_check(new_row, new_col, board, self._color):
                                    moves.append(Move((self._row, self._col), (new_row, new_col), board))


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
        # Allow player to pass
        moves.append(Move((self._row, self._col), (self._row, self._col), board))

        poss_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        blue_palace = [(9, 3), (9, 5), (7, 3), (7, 5), (8, 4)]
        red_palace = [(0, 3), (0, 5), (2, 3), (2, 5), (1, 4)]
        palace_moves = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

        if self.get_color() == 'r':
            for row, col in poss_moves:
                new_row, new_col = self._row + row, self._col + col
                if self.red_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))

        if self.get_color() == 'b':
            for row, col in poss_moves:
                new_row, new_col = self._row + row, self._col + col
                if self.blue_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))

        if self.get_orig() in red_palace:
            for row, col in palace_moves:
                new_row, new_col = self._row + row, self._col + col
                if self.red_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))

        if self.get_orig() in blue_palace:
            for row, col in palace_moves:
                new_row, new_col = self._row + row, self._col + col
                if self.blue_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))



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
        General(self.get_color(), self.get_row(), self.get_col()).get_legal_moves(board, moves)
        return moves



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
        # Allow player to pass
        moves.append(Move((self._row, self._col), (self._row, self._col), board))

        poss_moves = ((-1, 0), (1, 0), (0, -1), (0, 1))
        directions = [-1, 1]

        for row, col in poss_moves:
            new_row, new_col = self._row + row, self._col + col
            if 0 < new_row < 9 and 0 < new_col < 8:
                if board[new_row][new_col] is None:
                    new_row += row
                    new_col += col
                    if row == 0:
                        for direction in directions:
                            new_row = self._row + direction
                            if self.valid_space_check(new_row, new_col, board, self._color):
                                moves.append(Move((self._row, self._col), (new_row, new_col), board))
                    if col == 0:
                        for direction in directions:
                            new_col = self._col + direction
                            if self.valid_space_check(new_row, new_col, board, self._color):
                                moves.append(Move((self._row, self._col), (new_row, new_col), board))



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
        # Allow player to pass
        moves.append(Move((self._row, self._col), (self._row, self._col), board))

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
    This class is used to create a Move object for each move as it is passed by the user. Stores the starting and
    ending locations, the moving piece, and any piece that may be at the destination square. This class relies on
    the Piece class to create valid moves. Information stored in this class can be used to easily undo moves
    if a check or otherwise invalid move is discovered.
    """
    def __init__(self, orig, dest, cur_board):
        self._orig_row = orig[0]
        self._orig_col = orig[1]
        self._dest_row = dest[0]
        self._dest_col = dest[1]
        self._piece = cur_board[self._orig_row][self._orig_col]
        self._target = cur_board[self._dest_row][self._dest_col]
        self._cur_board = cur_board
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

    def __eq__(self, other):
        """
        This is used to equate the move objects generated in the "make_move" function which are created by the user's
        string input to the list of valid moves generated within the Move class. Even though the moves look equal,
        Python does not inherently know how to equate them so by generating a 4 digit "ID" of the origin and destination
        coordinates of a move, two Moves can be equated as long as their ID matches.
        """
        if isinstance(other, Move):
            return self._moveID == other._moveID
        return False

"""
DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS
Initializing the board:
    My program initializes the board when the JanggiGame class is called by generating a defined list of lists. As the
    board is generated, Piece objects are created for each piece on the board which have their color and original
    coordinates stored for easy access later on. By rule, the active turn is set to 'b' for Blue and the game state
    is set to 'UNFINISHED.
    
Determining how to represent pieces  at a given location on the board:
    I elected to create a Piece class. I began by using a text notation to store piece information on the board
     but this got to be a bit cumbersome as the project progressed. I reworked my program to use a Piece object stored
     which is stored at a [row][column] index on the board and that information is stored in the Piece object. By
     representing the pieces as objects, it cleaned up the process of determining valid pieces. Instead of iterating
     through the board and matching strings to potential piece types, by using pieces I can directly access the
     valid move rules which I have written into a method in each piece subclass.
      
Determining how to validate a given move according to the rules for each piece, turn taking and other game rules.
    Currently, my program generates all possible moves for each piece, I have not yet accounted for check. I decided
    to implement it by iterating through the board and for each index which is not 'None' (an empty space), the
    get_valid_moves function calls "fill_possible_moves" which in turn calls the get_legal_moves method in the
    Piece object, passing it a current iteration of the board and the list of valid moves. Each piece then has an
    algorithm which iterates square by square away from the piece, according to the given piece rules, and if a square
    qualifies as a valid move, a Move object is created from the starting square to that target square. When a player
    attempts to play a move, the "active_turn" value is compared to the color stored in the piece object and if those
    do not match, the player is not attempting to move their opponent's pieces and the move is disallowed.
    
    Now that my program generates a full list of possible moves at any given time, I plan to implement my 
    "get_valid_moves" function which will filter out any of the possible moves which would violate other game rules
    such as revealing a check.
    
    My is_in_check function keeps track of the current location of each General at a given time. In order to screen
    for moves which would reveal a check my plan is to:
    - Iterate through the board generating possible moves for each piece
    - For each possible move, make the move
    - Iterate through the board generating possible opponent moves
    - If General is now in check, previous move revealed it and it must be undone and that move removed from valid moves
    
Modifying the board state after each move.
    By using Move objects to handle my moves, I am storing the piece which was moved and the piece which was removed
    as well as the starting and ending coordinates. This information is passed to the make_move function and used
    to set the original square to a None value and the destination is overwritten with the original piece. 
    
Determining how to track which player's turn it is to play right now.
    I initiated an "active_turn" data member in my JanggiGame class which stores either 'b' or 'r'. By rule, the blue
    player initiates so active_turn is initiated as 'b'. After making a valid move, the "set_next_turn" method checks
    if "active_turn == 'b'" and if so, sets it to 'r', otherwise sets it to 'b'. By alternating this data member between
    'b' and 'r' and comparing it to the color value stored within each Piece object, I can make sure that players are
    not playing out of turn or moving their opponents pieces.
    
Determining how to detect the checkmate scenario.
    - Iterate through the board generating all valid moves
    - If a move attacks the opponent's general:
    - Generate valid moves for the General and check if there are any valid moves which escape check
    - If not, check all valid moves for the defending player to test whether any moves block the attacker
    - If defender has a move which blocks the attack, general is not in checkmate
    - If general does not have any valid moves and defender does not have any possible moves which block the attack,
        General is in checkmate
        
Determining which player has won and also figuring out when to check that.
    - After each move, call 'is_in_check' with the opponent's color passed as parameter
    - If 'is_in_check' returns true, generate possible moves for the general in check
    - If the general cannot escape check, generate all possible moves for that player and check if
        they are able to block the check
    - If the general does not have any valid moves and the defender cannot block, general is in checkmate, update
        status to 'PLAYER_WON' where PLAYER is the color which matches "active_turn".
"""