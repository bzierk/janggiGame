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
        self._active_turn = 'blue'
        self._board = [
            [Chariot('red', 0, 0), Elephant('red', 0, 1), Horse('red', 0, 2), Guard('red', 0, 3), None,
             Guard('red', 0, 5), Elephant('red', 0, 6), Horse('red', 0, 7), Chariot('red', 0, 8)],
            [None, None, None, None, General('red', 1, 4), None, None, None, None],
            [None, Cannon('red', 2, 1), None, None, None, None, None, Cannon('red', 2, 7), None],
            [Soldier('red', 3, 0), None, Soldier('red', 3, 2), None, Soldier('red', 3, 4), None, Soldier('red', 3, 6),
             None, Soldier('red', 3, 8)],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [Soldier('blue', 6, 0), None, Soldier('blue', 6, 2), None, Soldier('blue', 6, 4), None,
             Soldier('blue', 6, 6), None, Soldier('blue', 6, 8)],
            [None, Cannon('blue', 7, 1), None, None, None, None, None, Cannon('blue', 7, 7), None],
            [None, None, None, None, General('blue', 8, 4), None, None, None, None],
            [Chariot('blue', 9, 0), Elephant('blue', 9, 1), Horse('blue', 9, 2), Guard('blue', 9, 3), None,
             Guard('blue', 9, 5), Elephant('blue', 9, 6), Horse('blue', 9, 7), Chariot('blue', 9, 8)],
        ]
        self._game_state = 'UNFINISHED'
        self._red_general = (1, 4)
        self._blue_general = (8, 4)

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
        if self._active_turn == 'blue':
            self._active_turn = 'red'
        else:
            self._active_turn = 'blue'

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
        opponent = {'red': 'blue', 'blue': 'red'}
        vuln_squares = set()
        counter_moves = self.fill_possible_moves(opponent[color])

        for move in counter_moves:
            print("piece color", move.get_original_piece().get_color())
            vuln_squares.add(move.get_target())
        if self.get_general_loc(color) in vuln_squares:
            return True
        return False

    def get_general_loc(self, color):
        """
        Returns the current row and column for the general of a specified color.
        """
        if color == 'red':
            return self._red_general
        else:
            return self._blue_general

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

        if len(self.get_valid_moves(self._active_turn)) == 0:
            if self._active_turn == 'blue':
                print('RED WON')
                self.set_game_state('RED_WON')
            else:
                print('BLUE WON')
                self.set_game_state('BLUE_WON')

        move = Move(orig_pair, dest_pair, self._board)

        if move not in self.get_valid_moves(self._active_turn):
            return False

        if move.get_orig() == move.get_target():
            if not self.is_in_check(self._active_turn):
                self.set_next_turn()
                return True

        return self.make_move_helper(move)

    def make_move_helper(self, move):
        """
        Helper function which takes a Move class object as a parameter and uses the information within the object
        to update the board and update the information within the appropriate Piece class objects. If a general is
        moved, updates the general's location in the JanggiGame class so that it can be easily referenced for
        "check" verifications.
        """
        if self._game_state != 'UNFINISHED':
            return False

        orig_piece = move.get_original_piece()
        self._board[move.get_orig()[0]][move.get_orig()[1]] = None
        self._board[move.get_target()[0]][move.get_target()[1]] = orig_piece
        orig_piece.set_row(move.get_target()[0])
        orig_piece.set_col(move.get_target()[1])

        if orig_piece.get_name() == 'General':
            if orig_piece.get_color() == 'red':
                self._red_general = (move.get_target()[0], move.get_target()[1])
            else:
                self._blue_general = (move.get_target()[0], move.get_target()[1])

        self.set_next_turn()
        return True

    def fill_possible_moves(self, color):
        """
        This function generates all possible moves for a player, regardless of whether or not the move would leave
        that player's general in check.
        """
        possible_moves = []
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                if self._board[row][col] is not None:
                    if self._board[row][col].get_color() == color:
                        self._board[row][col].get_legal_moves(self._board, possible_moves)

        return possible_moves

    def get_valid_moves(self, color):
        """
        Takes a set of all possible moves for a color according to the individual pieces' move rules and verifies
        that they do not violate other rules by leaving their own General in check. For each possible move,
        makes that move, generates the opponents possible moves, and checks if the General has been place in check,
        if so that move is removed from the list of valid moves and the next move is checked. The list of valid
        moves which is returned meets the movement rules for a given piece and does not leave the General open to a
        revealed check.
        """
        valid_moves = self.fill_possible_moves(color)

        for i in range(len(valid_moves)-1, -1, -1):
            temp_move = valid_moves[i]
            self.make_move_helper(valid_moves[i])
            self.set_next_turn()
            if self.is_in_check(self._active_turn):
                valid_moves.remove(valid_moves[i])
            self.set_next_turn()
            self._board[temp_move.get_orig()[0]][temp_move.get_orig()[1]] = temp_move.get_original_piece()
            self._board[temp_move.get_target()[0]][temp_move.get_target()[1]] = temp_move.get_target_piece()
            self.set_next_turn()

        return valid_moves


def valid_space_check(row, col, board, my_color):
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


def blue_palace_check(row, col, board, my_color):
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


def is_in_palace(row, col):
    """
    If a coordinate is in the palace, returns True, if coordinate is outside of the palace, returns False.
    """
    if (9 >= row >= 7) or (2 >= row >= 0):
        if 5 >= col >= 3:
            return True

    return False


def red_palace_check(row, col, board, my_color):
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
                while is_in_palace(new_row, new_col):
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
            while valid_space_check(new_row, new_col, board, self._color):
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
                while red_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))
                    if board[new_row][new_col] is not None and board[new_row][new_col].get_color() != self._color:
                        break
                    new_row += row
                    new_col += col

        # handles diagonal moves if chariot is in the blue palace
        if self.get_orig() in blue_palace:
            for row, col in palace_moves:
                new_row, new_col = self._row + row, self._col + col
                while blue_palace_check(new_row, new_col, board, self._color):
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
            if 0 <= new_row <= 9 and 0 <= new_col <= 8:
                if board[new_row][new_col] is None:
                    new_row += row
                    new_col += col
                    temp_coords = [new_row, new_col]
                    if 0 <= new_row <= 9 and 0 <= new_col <= 8:
                        if row == 0:
                            for direction in directions:
                                new_col = temp_coords[1]
                                new_row = self._row + direction
                                if 0 <= new_row <= 9 and 0 <= new_col <= 8:
                                    if board[new_row][new_col] is None:
                                        new_row += direction
                                        new_col = new_col + col
                                        if valid_space_check(new_row, new_col, board, self._color):
                                            moves.append(Move((self._row, self._col), (new_row, new_col), board))

                        if col == 0:
                            for direction in directions:
                                new_row = temp_coords[0]
                                new_col = self._col + direction
                                if 0 <= new_row <= 9 and 0 <= new_col <= 8:
                                    if board[new_row][new_col] is None:
                                        new_row = new_row + row
                                        new_col += direction
                                        if valid_space_check(new_row, new_col, board, self._color):
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

        if self.get_color() == 'red':
            for row, col in poss_moves:
                new_row, new_col = self._row + row, self._col + col
                if red_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))

        if self.get_color() == 'blue':
            for row, col in poss_moves:
                new_row, new_col = self._row + row, self._col + col
                if blue_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))

        if self.get_orig() in red_palace:
            for row, col in palace_moves:
                new_row, new_col = self._row + row, self._col + col
                if red_palace_check(new_row, new_col, board, self._color):
                    moves.append(Move((self._row, self._col), (new_row, new_col), board))

        if self.get_orig() in blue_palace:
            for row, col in palace_moves:
                new_row, new_col = self._row + row, self._col + col
                if blue_palace_check(new_row, new_col, board, self._color):
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
            if 0 <= new_row <= 9 and 0 <= new_col <= 8:
                if board[new_row][new_col] is None:
                    new_row += row
                    new_col += col
                    if 0 <= new_row <= 9 and 0 <= new_col <= 8:
                        if row == 0:
                            for direction in directions:
                                new_row = self._row + direction
                                if valid_space_check(new_row, new_col, board, self._color):
                                    moves.append(Move((self._row, self._col), (new_row, new_col), board))
                        if col == 0:
                            for direction in directions:
                                new_col = self._col + direction
                                if valid_space_check(new_row, new_col, board, self._color):
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

        direction = {'red': 1, 'blue': -1}
        poss_moves = ((0, -1), (0, 1), (direction[self._color], 0))

        for row, col in poss_moves:
            new_row, new_col = self._row + row, self._col + col
            if valid_space_check(new_row, new_col, board, self._color):
                moves.append(Move((self._row, self._col), (new_row, new_col), board))

        blue_palace = [(9, 3), (9, 5)]
        red_palace = [(0, 3), (0, 5)]
        if self._row == 1 and self._col == 4:
            for row, col in red_palace:
                if valid_space_check(row, col, board, self._color):
                    moves.append(Move((self._row, self._col), (row, col), board))

        if self._row == 8 and self._col == 4:
            for row, col in blue_palace:
                if valid_space_check(row, col, board, self._color):
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
        self._orig = orig
        self._dest = dest
        self._piece = cur_board[self._orig[0]][self._orig[1]]
        self._target = cur_board[self._dest[0]][self._dest[1]]
        self._cur_board = cur_board
        self._moveID = self._orig[0] * 1000 + self._orig[1] * 100 + self._dest[0] * 10 + self._dest[1]

    def get_orig(self):
        """
        Returns the origin coordinates of a desired move
        """
        return self._orig[0], self._orig[1]

    def get_target(self):
        """
        Returns the target of a move
        """
        return self._dest[0], self._dest[1]

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

gs = JanggiGame()
gs.make_move('c10', 'd8')
gs.make_move('h1', 'i3')
gs.make_move('a10', 'a9')
gs.make_move('i4', 'i5')
gs.make_move('a9', 'a8')
gs.make_move('i3', 'h5')