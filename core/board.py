# core/board.py

from config import BOARD_SIZE, WIN_LENGTH, EMPTY, PLAYER_X, PLAYER_O


class Board:
    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.last_move = None
        self.move_history = []

    def is_valid_move(self, row: int, col: int) -> bool:
        return (
            0 <= row < BOARD_SIZE
            and 0 <= col < BOARD_SIZE
            and self.board[row][col] == EMPTY
        )

    def get_valid_moves(self) -> list[tuple[int, int]]:
        moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == EMPTY:
                    moves.append((r, c))
        return moves

    def make_move(self, row: int, col: int, player: str) -> bool:
        if player not in (PLAYER_X, PLAYER_O):
            return False
        if not self.is_valid_move(row, col):
            return False

        self.board[row][col] = player
        self.last_move = (row, col)
        self.move_history.append((row, col))
        return True

    def undo_move(self, row: int, col: int) -> None:
        if not self.move_history:
            return
        if self.move_history[-1] != (row, col):
            return

        self.move_history.pop()
        self.board[row][col] = EMPTY
        self.last_move = self.move_history[-1] if self.move_history else None

    def clone(self) -> "Board":
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        new_board.last_move = self.last_move
        new_board.move_history = self.move_history[:]
        return new_board

    def check_winner(self) -> str | None:
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                player = self.board[r][c]
                if player == EMPTY:
                    continue

                for dr, dc in directions:
                    count = 1
                    nr, nc = r + dr, c + dc
                    while (
                        0 <= nr < BOARD_SIZE
                        and 0 <= nc < BOARD_SIZE
                        and self.board[nr][nc] == player
                    ):
                        count += 1
                        if count >= WIN_LENGTH:
                            return player
                        nr += dr
                        nc += dc

        return None

    def is_full(self) -> bool:
        return all(
            self.board[r][c] != EMPTY
            for r in range(BOARD_SIZE)
            for c in range(BOARD_SIZE)
        )

    def is_terminal(self) -> tuple[bool, str | None]:
        winner = self.check_winner()
        if winner is not None:
            return (True, winner)
        if self.is_full():
            return (True, "DRAW")
        return (False, None)