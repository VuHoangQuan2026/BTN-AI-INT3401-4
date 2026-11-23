# agents/random_agent.py

import random
import time

from agents.base_agent import BaseAgent


class RandomAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def choose_move(self, board, player):
        self.reset_stats()
        start_time = time.perf_counter()

        valid_moves = board.get_valid_moves()
        if not valid_moves:
            self.stats["time_taken"] = time.perf_counter() - start_time
            return None

        move = random.choice(valid_moves)
        self.stats["last_move"] = move
        self.stats["nodes_visited"] = len(valid_moves)
        self.stats["time_taken"] = time.perf_counter() - start_time
        return move
