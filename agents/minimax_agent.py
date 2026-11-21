# agents/minimax_agent.py

import math
import time

from agents.base_agent import BaseAgent
from config import BOARD_SIZE, WIN_LENGTH, EMPTY, PLAYER_X, PLAYER_O, DEFAULT_DEPTH


class MiniMaxAgent(BaseAgent):
    def __init__(self, depth: int = DEFAULT_DEPTH, search_radius: int = 1):
        super().__init__()
        self.depth = max(1, depth)
        self.search_radius = search_radius

    def _get_opponent(self, player: str) -> str:
        return PLAYER_O if player == PLAYER_X else PLAYER_X

    def get_candidate_moves(self, board) -> list[tuple[int, int]]:
        candidates = set()
        has_piece = False

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board.board[r][c] != EMPTY:
                    has_piece = True
                    for dr in range(-self.search_radius, self.search_radius + 1):
                        for dc in range(-self.search_radius, self.search_radius + 1):
                            nr, nc = r + dr, c + dc
                            if board.is_valid_move(nr, nc):
                                candidates.add((nr, nc))

        if not has_piece:
            center = BOARD_SIZE // 2
            return [(center, center)]

        return sorted(candidates)

    def evaluate(self, board, player: str, remaining_depth: int = 0) -> float:
        opponent = self._get_opponent(player)
        is_over, winner = board.is_terminal()

        if is_over:
            if winner == player:
                return 1_000_000 + remaining_depth
            if winner == opponent:
                return -1_000_000 - remaining_depth
            return 0

        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell = board.board[r][c]
                if cell == EMPTY:
                    continue

                for dr, dc in directions:
                    prev_r, prev_c = r - dr, c - dc
                    if (
                        0 <= prev_r < BOARD_SIZE
                        and 0 <= prev_c < BOARD_SIZE
                        and board.board[prev_r][prev_c] == cell
                    ):
                        continue

                    length = 0
                    nr, nc = r, c
                    while (
                        0 <= nr < BOARD_SIZE
                        and 0 <= nc < BOARD_SIZE
                        and board.board[nr][nc] == cell
                    ):
                        length += 1
                        nr += dr
                        nc += dc

                    open_ends = 0
                    if (
                        0 <= prev_r < BOARD_SIZE
                        and 0 <= prev_c < BOARD_SIZE
                        and board.board[prev_r][prev_c] == EMPTY
                    ):
                        open_ends += 1
                    if (
                        0 <= nr < BOARD_SIZE
                        and 0 <= nc < BOARD_SIZE
                        and board.board[nr][nc] == EMPTY
                    ):
                        open_ends += 1

                    pattern_score = self._score_pattern(length, open_ends)
                    if cell == player:
                        score += pattern_score
                    else:
                        score -= int(pattern_score * 1.1)

        return score

    def _score_pattern(self, length: int, open_ends: int) -> int:
        if length >= WIN_LENGTH:
            return 100_000
        if open_ends == 0:
            return 0
        if length == 4:
            return 10_000 if open_ends == 2 else 1_500
        if length == 3:
            return 1_000 if open_ends == 2 else 150
        if length == 2:
            return 100 if open_ends == 2 else 20
        if length == 1:
            return 10 if open_ends == 2 else 2
        return 0

    def _minimax(self, board, depth: int, is_maximizing: bool, root_player: str) -> float:
        self.stats["nodes_visited"] += 1

        is_over, _ = board.is_terminal()
        if depth == 0 or is_over:
            return self.evaluate(board, root_player, remaining_depth=depth)

        current_player = root_player if is_maximizing else self._get_opponent(root_player)
        moves = self.get_candidate_moves(board)

        if is_maximizing:
            best_val = -math.inf
            for r, c in moves:
                board.make_move(r, c, current_player)
                val = self._minimax(board, depth - 1, False, root_player)
                board.undo_move(r, c)
                if val > best_val:
                    best_val = val
            return best_val
        else:
            best_val = math.inf
            for r, c in moves:
                board.make_move(r, c, current_player)
                val = self._minimax(board, depth - 1, True, root_player)
                board.undo_move(r, c)
                if val < best_val:
                    best_val = val
            return best_val

    def choose_move(self, board, player: str) -> tuple[int, int] | None:
        self.reset_stats()
        self.stats["depth"] = self.depth
        start_time = time.perf_counter()

        if not board.get_valid_moves():
            self.stats["time_taken"] = time.perf_counter() - start_time
            return None

        board_copy = board.clone()
        candidate_moves = self.get_candidate_moves(board_copy)

        best_move = candidate_moves[0]
        best_val = -math.inf

        for r, c in candidate_moves:
            board_copy.make_move(r, c, player)
            val = self._minimax(board_copy, self.depth - 1, False, player)
            board_copy.undo_move(r, c)

            if val > best_val:
                best_val = val
                best_move = (r, c)

        self.stats["last_move"] = best_move
        self.stats["time_taken"] = time.perf_counter() - start_time
        return best_move

    def format_stats(self) -> str:
        return (
            f"[MiniMax] move={self.stats['last_move']} | "
            f"depth={self.stats.get('depth', self.depth)} | "
            f"nodes={self.stats['nodes_visited']} | "
            f"time={self.stats['time_taken']:.4f}s"
        )