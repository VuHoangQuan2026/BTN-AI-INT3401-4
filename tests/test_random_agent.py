# tests/test_random_agent.py

import unittest
from core.board import Board
from agents.random_agent import RandomAgent
from config import BOARD_SIZE, PLAYER_X, PLAYER_O


class TestRandomAgent(unittest.TestCase):
    def test_returns_valid_move_without_modifying_board(self):
        board = Board()
        board.make_move(4, 4, PLAYER_X)
        snapshot = [row[:] for row in board.board]
        agent = RandomAgent()
        move = agent.choose_move(board, PLAYER_O)

        self.assertTrue(board.is_valid_move(*move))
        self.assertEqual(board.board, snapshot)
        self.assertEqual(agent.stats["last_move"], move)
        self.assertEqual(agent.stats["nodes_visited"], BOARD_SIZE * BOARD_SIZE - 1)

    def test_returns_none_when_full(self):
        board = Board()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                board.make_move(r, c, PLAYER_X)
        self.assertIsNone(RandomAgent().choose_move(board, PLAYER_O))


if __name__ == "__main__":
    unittest.main()
