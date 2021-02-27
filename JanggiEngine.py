# Author: Bryan Zierk
# Date: 2/26/21
# Description:

class GameState:
    def __init__(self):
        """
        Builds the Janggi board. A rectangular board with lines creating intersections in a 9x10 grid on which
        pieces can be placed.
        """
        self._board = [
            ['rChariot', 'rElephant', 'rHorse', 'rGuard', '--', 'rGuard', 'rElephant', 'rHorse', 'rChariot'],
            ['--', '--', '--', '--', 'rGeneral', '--', '--', '--', '--'],
            ['--', 'rCannon', '--', '--', '--', '--', '--', 'rCannon', '--'],
            ['rSoldier', '--', 'rSoldier', '--', 'rSoldier', '--', 'rSoldier', '--', 'rSoldier'],
            ['--', '--', '--', '--', '--', ],
            ['--', '--', '--', '--', '--', ],
            ['bSoldier', '--', 'bSoldier', '--', 'bSoldier', '--', 'bSoldier', '--', 'bSoldier'],
            ['--', 'bCannon', '--', '--', '--', '--', '--', 'bCannon', '--'],
            ['--', '--', '--', '--', 'bGeneral', '--', '--', '--', '--'],
            ['bChariot', 'bElephant', 'bHorse', 'bGuard', '--', 'bGuard', 'bElephant', 'bHorse', 'bChariot'],
        ]

    def get_board(self):
        return self._board
