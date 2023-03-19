# Author: Carolynn Wicker
# GitHub username: wickerc
# Date: 03/18/2023
# Description: Unit tests for the classes in CheckersGame.py. It has at least five unit tests and uses at least two
# different assert functions.

import unittest
from CheckersGame import Checkers
from CheckersGame import Player


class CheckersTests(unittest.TestCase):
    """Contains unit tests for the Checkers class"""

    def test_1(self):
        """Tests init method and get methods to check if new Checkers game initializes the first player's turn to None,
        prior to players being created"""
        new_game = Checkers()
        self.assertEqual(new_game.get_players_turn(), None)

    def test_2(self):
        """Tests create_player method, checks that it adds new player name and object to the correct lists and
        sets the players_turn (first player) to the player with the black pieces"""
        new_game = Checkers()
        player_1 = new_game.create_player("Connor", "White")
        player_2 = new_game.create_player("Carolynn", "Black")
        self.assertIn("Connor", new_game._players_list)
        self.assertIn("Carolynn", new_game._players_list)
        self.assertEqual("Carolynn", new_game.get_players_turn())

    def test_3(self):
        """Tests play_game and get_checker_details methods to make board reflects recent move"""
        new_game = Checkers()
        player_1 = new_game.create_player("Connor", "White")
        player_2 = new_game.create_player("Carolynn", "Black")
        new_game.play_game("Carolynn", (5, 0), (4, 1))
        self.assertEqual(new_game.get_checker_details((4, 1)), "Black")
        self.assertEqual(new_game.get_checker_details((5, 0)), None)


if __name__ == '__main__':
  unittest.main()