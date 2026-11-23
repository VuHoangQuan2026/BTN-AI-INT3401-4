# main.py

from core.board import Board
from core.game_engine import GameEngine
from agents.random_agent import RandomAgent
from agents.minimax_agent import MiniMaxAgent
from ui.pygame_ui import PygameUI


def main():
    board = Board()
    agent_x = None
    agent_o = MiniMaxAgent()
    engine = GameEngine(board, agent_x, agent_o)
    ui = PygameUI(engine)
    ui.run()


if __name__ == "__main__":
    main()
