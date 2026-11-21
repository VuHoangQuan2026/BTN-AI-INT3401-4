# agents/base_agent.py

from abc import ABC, abstractmethod
import time


class BaseAgent(ABC):
    def __init__(self):
        self.stats = {
            "last_move": None,
            "time_taken": 0.0,
            "nodes_visited": 0,
        }

    def reset_stats(self):
        self.stats = {
            "last_move": None,
            "time_taken": 0.0,
            "nodes_visited": 0,
        }

    @abstractmethod
    def choose_move(self, board, player):
        pass