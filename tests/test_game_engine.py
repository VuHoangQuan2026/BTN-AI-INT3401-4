# tests/test_game_engine.py

import unittest
from core.board import Board
from core.game_engine import GameEngine
from agents.random_agent import RandomAgent
from config import PLAYER_X, PLAYER_O, EMPTY, BOARD_SIZE


class TestGameEngine(unittest.TestCase):
    def test_initial_state(self):
        e = GameEngine(Board(), None, RandomAgent())
        self.assertEqual(e.current_player, PLAYER_X)
        self.assertFalse(e.game_over)
        self.assertIsNone(e.winner)
        self.assertTrue(e.is_human_turn())

    def test_human_move_then_ai_turn(self):
        e = GameEngine(Board(), None, RandomAgent())
        self.assertTrue(e.make_move(4, 4))
        self.assertEqual(e.current_player, PLAYER_O)
        self.assertFalse(e.is_human_turn())
        self.assertFalse(e.make_move(0, 0))  # không phải lượt người
        self.assertTrue(e.play_ai_turn())
        self.assertEqual(e.current_player, PLAYER_X)
        self.assertEqual(e.total_moves, 2)

    def test_invalid_moves(self):
        e = GameEngine(Board(), None, RandomAgent())
        self.assertTrue(e.make_move(1, 1))
        e.switch_turn()
        e.switch_turn()
        self.assertFalse(e.make_move(1, 1))
        self.assertFalse(e.make_move(-1, 0))
        self.assertFalse(e.make_move(0, BOARD_SIZE))

    def test_win_stops_game_and_reset(self):
        e = GameEngine(Board(), None, None)
        for i in range(5):
            self.assertTrue(e.make_move(0, i))      # X
            if i < 4:
                self.assertTrue(e.make_move(1, i))  # O
        self.assertTrue(e.game_over)
        self.assertEqual(e.winner, PLAYER_X)
        self.assertFalse(e.make_move(5, 5))

        e.reset_game()
        self.assertFalse(e.game_over)
        self.assertIsNone(e.winner)
        self.assertEqual(e.total_moves, 0)
        self.assertEqual(e.current_player, PLAYER_X)
        self.assertEqual(e.board.board[0][0], EMPTY)
        self.assertIsNone(e.board.last_move)

    def test_ai_vs_ai_runs_to_end_without_pygame(self):
        e = GameEngine(Board(), RandomAgent(), RandomAgent())
        while not e.game_over:
            self.assertTrue(e.play_ai_turn())
        self.assertIn(e.winner, (PLAYER_X, PLAYER_O, "DRAW"))
        self.assertIn("board", e.get_state())


if __name__ == "__main__":
    unittest.main()
