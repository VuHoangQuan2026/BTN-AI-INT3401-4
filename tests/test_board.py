# tests/test_board.py

import unittest
from core.board import Board
from agents.minimax_agent import MiniMaxAgent
from config import BOARD_SIZE, EMPTY, PLAYER_X, PLAYER_O


class TestBoardAndMiniMax(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board(self):
        self.assertEqual(len(self.board.board), BOARD_SIZE)
        self.assertEqual(len(self.board.board[0]), BOARD_SIZE)
        self.assertEqual(len(self.board.get_valid_moves()), 81)
        self.assertIsNone(self.board.last_move)
        self.assertEqual(self.board.is_terminal(), (False, None))

    def test_moves_and_validation(self):
        self.assertTrue(self.board.make_move(4, 4, PLAYER_X))
        self.assertFalse(self.board.make_move(4, 4, PLAYER_O))
        self.assertFalse(self.board.make_move(-1, 0, PLAYER_O))
        self.assertFalse(self.board.make_move(9, 5, PLAYER_O))
        self.assertFalse(self.board.make_move(0, 0, 'Z'))

    def test_undo_move(self):
        self.board.make_move(0, 0, PLAYER_X)
        self.board.make_move(0, 1, PLAYER_O)

        self.board.undo_move(0, 0)
        self.assertEqual(self.board.board[0][1], PLAYER_O)

        self.board.undo_move(0, 1)
        self.assertEqual(self.board.board[0][1], EMPTY)
        self.assertEqual(self.board.last_move, (0, 0))

    def test_clone_independence(self):
        self.board.make_move(2, 2, PLAYER_X)
        cloned = self.board.clone()
        cloned.make_move(3, 3, PLAYER_O)
        self.assertEqual(self.board.board[3][3], EMPTY)
        self.assertEqual(cloned.board[3][3], PLAYER_O)

    def test_win_four_directions(self):
        directions = [
            [(0, c) for c in range(5)],
            [(r, 0) for r in range(5)],
            [(i, i) for i in range(5)],
            [(i, 4 - i) for i in range(5)],
        ]
        for coords in directions:
            b = Board()
            for r, c in coords:
                b.make_move(r, c, PLAYER_X)
            self.assertEqual(b.is_terminal(), (True, PLAYER_X))

    def test_draw_when_full_without_winner(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                player = PLAYER_X if (r + (c // 2)) % 2 == 0 else PLAYER_O
                self.board.make_move(r, c, player)

        self.assertTrue(self.board.is_full())
        self.assertIsNone(self.board.check_winner())
        self.assertEqual(self.board.is_terminal(), (True, "DRAW"))

    def test_minimax_takes_winning_move(self):
        for c in range(1, 5):
            self.board.make_move(4, c, PLAYER_X)
        agent = MiniMaxAgent(depth=2)
        move = agent.choose_move(self.board, PLAYER_X)

        self.assertIn(move, [(4, 0), (4, 5)])
        self.assertGreater(agent.stats["nodes_visited"], 0)
        self.assertEqual(self.board.board[move[0]][move[1]], EMPTY)

    def test_minimax_blocks_opponent_four(self):
        for c in range(1, 5):
            self.board.make_move(4, c, PLAYER_X)
        self.board.make_move(4, 0, PLAYER_O)
        agent = MiniMaxAgent(depth=2)
        move = agent.choose_move(self.board, PLAYER_O)

        self.assertEqual(move, (4, 5))


if __name__ == "__main__":
    unittest.main()