# core/game_engine.py

from config import PLAYER_X, PLAYER_O


class GameEngine:
    def __init__(self, board, agent_x=None, agent_o=None):
        self.board = board
        self.agent_x = agent_x
        self.agent_o = agent_o

        self.current_player = PLAYER_X
        self.game_over = False
        self.winner = None
        self.total_moves = 0
        self.total_ai_time = 0.0

    def get_current_agent(self):
        return self.agent_x if self.current_player == PLAYER_X else self.agent_o

    def is_human_turn(self) -> bool:
        return self.get_current_agent() is None

    def make_move(self, row: int, col: int) -> bool:
        if self.game_over:
            return False
        if not self.is_human_turn():
            return False
        if not self.board.is_valid_move(row, col):
            return False
        if not self.board.make_move(row, col, self.current_player):
            return False

        self.total_moves += 1
        self.check_game_status()
        if not self.game_over:
            self.switch_turn()
        return True

    def play_ai_turn(self) -> bool:
        if self.game_over:
            return False
        agent = self.get_current_agent()
        if agent is None:
            return False

        move = agent.choose_move(self.board, self.current_player)
        if move is None:
            return False

        row, col = move
        if not self.board.make_move(row, col, self.current_player):
            return False

        self.total_moves += 1
        self.total_ai_time += agent.stats.get("time_taken", 0.0)
        self.check_game_status()
        if not self.game_over:
            self.switch_turn()
        return True

    def check_game_status(self) -> tuple[bool, str | None]:
        is_over, winner = self.board.is_terminal()
        if is_over:
            self.game_over = True
            self.winner = winner
        return (is_over, winner)

    def switch_turn(self) -> None:
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

    def reset_game(self) -> None:
        # Làm sạch bàn cờ tại chỗ để mọi tham chiếu tới board vẫn hợp lệ.
        # Chỉ dùng API của Board (undo_move) nên không phụ thuộc cấu trúc nội bộ.
        while self.board.move_history:
            r, c = self.board.move_history[-1]
            self.board.undo_move(r, c)

        self.current_player = PLAYER_X
        self.game_over = False
        self.winner = None
        self.total_moves = 0
        self.total_ai_time = 0.0
        for agent in (self.agent_x, self.agent_o):
            if agent is not None:
                agent.reset_stats()

    def get_state(self) -> dict:
        return {
            "board": self.board,
            "current_player": self.current_player,
            "game_over": self.game_over,
            "winner": self.winner,
            "total_moves": self.total_moves,
            "total_ai_time": self.total_ai_time,
        }
