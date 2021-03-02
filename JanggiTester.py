# Author: Bryan Zierk
# Date: 2/28/21
# Description: Testing file for JanggiGame

import unittest
from JanggiGame import *


class TestGanggi(unittest.TestCase):
    """
    Contains a series of unit tests for JanggiGame
    """
    def setUp(self):
        self.gs = JanggiGame()

    def test_first_turn(self):
        self.assertEqual(self.gs.active_turn(), 'b')
        self.gs.set_next_turn()
        self.assertEqual(self.gs.active_turn(), 'r')
        self.gs.set_next_turn()
        self.assertEqual(self.gs.active_turn(), 'b')

    def test_game_state(self):
        self.assertEqual(self.gs.get_game_state(), 'UNFINISHED')
        self.gs.set_game_state('BLUE WON')
        self.assertEqual(self.gs.get_game_state(), 'BLUE WON')

    def test_validate_move(self):
        test_soldier = Soldier('b', 3, 0)
        self.assertEqual(self.gs.validate_move('a1', 'a2', test_soldier), True)
        self.assertEqual(self.gs.validate_move('a0', 'a1', test_soldier), False)
        self.assertEqual(self.gs.validate_move('a10', 'a9', test_soldier), True)
        self.assertEqual(self.gs.validate_move('a11', 'a1', test_soldier), False)
        self.assertEqual(self.gs.validate_move('a1', 'j1', test_soldier), False)
        self.assertEqual(self.gs.validate_move('i10', 'a1', test_soldier), True)

    def test_make_move(self):
        self.assertEqual(self.gs.active_turn(), 'b')
        self.gs.make_move('a10', 'a9')
        self.assertEqual(self.gs.active_turn(), 'r')
        self.gs.make_move('a1', 'a2')
        self.assertEqual(self.gs.active_turn(), 'b')

    def test_set(self):
        moves = set()
        moves.add((2, 1))
        self.assertEqual((2,1) in moves, True)



