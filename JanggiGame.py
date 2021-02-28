"""

"""

class GameState:
    def __init__(self):
        """
        Builds the Janggi board. A rectangular board with lines creating 90 intersections in a 9x10 grid on which
        pieces can be placed.
        """
        self._blue_to_play = True
        self._board = [
            ['rChariot', 'rElephant', 'rHorse', 'rGuard', '--', 'rGuard', 'rElephant', 'rHorse', 'rChariot'],
            ['--', '--', '--', '--', 'rGeneral', '--', '--', '--', '--'],
            ['--', 'rCannon', '--', '--', '--', '--', '--', 'rCannon', '--'],
            ['rSoldier', '--', 'rSoldier', '--', 'rSoldier', '--', 'rSoldier', '--', 'rSoldier'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['bSoldier', '--', 'bSoldier', '--', 'bSoldier', '--', 'bSoldier', '--', 'bSoldier'],
            ['--', 'bCannon', '--', '--', '--', '--', '--', 'bCannon', '--'],
            ['--', '--', '--', '--', 'bGeneral', '--', '--', '--', '--'],
            ['bChariot', 'bElephant', 'bHorse', 'bGuard', '--', 'bGuard', 'bElephant', 'bHorse', 'bChariot'],
        ]

    def get_board(self):
        """
        Returns a list of lists which represent the current board setup
        """
        return self._board

    def blue_to_play(self):
        """
        If it is blue's turn, returns True, if red, returns False.
        """
        return self._blue_to_play

    def set_blue_to_play(self):
        """
        If blue_to_play is True, sets it to False, otherwise sets to True.
        """
        if self._blue_to_play is True:
            self._blue_to_play = False
        else:
            self._blue_to_play = True


class JanggiGame:
    """
    Creates a JanggiGame object which can be used to play Janggi
    """
    def __init__(self):
        """
        Initializes data members for JanggiGame
        """
        self._game_state = 'UNFINISHED'

    def get_game_state(self):
        """
        Returns the current game state
        """
        return self._game_state

    def is_in_check(self, color):
        """
        Takes 'red' or 'blue' as a parameter and checks if that color's General is in check. Returns True if the
        general is in check, otherwise returns False
        """
        pass

    def make_move(self, orig, dest):
        """
        Takes two strings as parameters which represent the square which a piece is moving from and moving to. The
        squares should be identified using algebraic notation with columns labeled a-i and rows labeled 1-10 where
        row 1 is the Red side and row 10 is the Blue side.
        """

