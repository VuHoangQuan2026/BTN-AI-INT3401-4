# ui/pygame_ui.py

import pygame

from config import (
    BOARD_SIZE,
    CELL_SIZE,
    BOARD_MARGIN,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    EMPTY,
    PLAYER_X,
    PLAYER_O,
)

BG_COLOR = (245, 222, 179)
LINE_COLOR = (60, 40, 20)
X_COLOR = (200, 30, 30)
O_COLOR = (30, 60, 200)
TEXT_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 80)
BUTTON_TEXT_COLOR = (255, 255, 255)
LAST_MOVE_COLOR = (255, 215, 0)


class PygameUI:
    def __init__(self, engine):
        self.engine = engine
        self.screen = None
        self.clock = None
        self.running = True
        self.font = None
        self.big_font = None
        self.restart_rect = pygame.Rect(
            WINDOW_WIDTH - BOARD_MARGIN - 110, WINDOW_HEIGHT - 55, 110, 36
        )

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Caro AI 9x9")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 18)
        self.big_font = pygame.font.SysFont("arial", 30, bold=True)

    def _cell_center(self, row, col):
        x = BOARD_MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        y = BOARD_MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        return x, y

    def draw_board(self):
        self.screen.fill(BG_COLOR)
        size = BOARD_SIZE * CELL_SIZE

        for i in range(BOARD_SIZE + 1):
            offset = BOARD_MARGIN + i * CELL_SIZE
            pygame.draw.line(self.screen, LINE_COLOR,
                             (BOARD_MARGIN, offset), (BOARD_MARGIN + size, offset), 2)
            pygame.draw.line(self.screen, LINE_COLOR,
                             (offset, BOARD_MARGIN), (offset, BOARD_MARGIN + size), 2)

        for i in range(BOARD_SIZE):
            label = self.font.render(str(i), True, TEXT_COLOR)
            cx, _ = self._cell_center(0, i)
            self.screen.blit(label, (cx - label.get_width() // 2,
                                     BOARD_MARGIN - label.get_height() - 4))
            _, cy = self._cell_center(i, 0)
            self.screen.blit(label, (BOARD_MARGIN - label.get_width() - 8,
                                     cy - label.get_height() // 2))

    def draw_pieces(self, board):
        last = board.last_move
        if last is not None:
            lx, ly = self._cell_center(*last)
            pygame.draw.rect(
                self.screen, LAST_MOVE_COLOR,
                (lx - CELL_SIZE // 2 + 2, ly - CELL_SIZE // 2 + 2,
                 CELL_SIZE - 4, CELL_SIZE - 4), 3,
            )

        radius = CELL_SIZE // 2 - 10
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell = board.board[r][c]
                if cell == EMPTY:
                    continue
                x, y = self._cell_center(r, c)
                if cell == PLAYER_X:
                    pygame.draw.line(self.screen, X_COLOR,
                                     (x - radius, y - radius), (x + radius, y + radius), 5)
                    pygame.draw.line(self.screen, X_COLOR,
                                     (x - radius, y + radius), (x + radius, y - radius), 5)
                elif cell == PLAYER_O:
                    pygame.draw.circle(self.screen, O_COLOR, (x, y), radius, 5)

    def draw_status(self):
        state = self.engine.get_state()
        y = BOARD_MARGIN + BOARD_SIZE * CELL_SIZE + 12

        if state["game_over"]:
            if state["winner"] == "DRAW":
                text = "DRAW!"
            else:
                text = f"{state['winner']} WINS!"
            line1 = self.big_font.render(text, True, TEXT_COLOR)
        else:
            who = "Human" if self.engine.is_human_turn() else "AI"
            line1 = self.font.render(
                f"Turn: {state['current_player']} ({who})", True, TEXT_COLOR)
        self.screen.blit(line1, (BOARD_MARGIN, y))

        info = (f"Moves: {state['total_moves']}   "
                f"AI time: {state['total_ai_time']:.3f}s   [R] restart  [ESC] quit")
        self.screen.blit(self.font.render(info, True, TEXT_COLOR), (BOARD_MARGIN, y + 36))

        pygame.draw.rect(self.screen, BUTTON_COLOR, self.restart_rect, border_radius=6)
        label = self.font.render("Restart", True, BUTTON_TEXT_COLOR)
        self.screen.blit(label, (self.restart_rect.centerx - label.get_width() // 2,
                                 self.restart_rect.centery - label.get_height() // 2))

    def pixel_to_cell(self, x, y):
        if x < BOARD_MARGIN or y < BOARD_MARGIN:
            return None
        col = (x - BOARD_MARGIN) // CELL_SIZE
        row = (y - BOARD_MARGIN) // CELL_SIZE
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return (int(row), int(col))
        return None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.engine.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.restart_rect.collidepoint(event.pos):
                    self.engine.reset_game()
                    continue
                cell = self.pixel_to_cell(*event.pos)
                if cell is None:
                    continue
                if self.engine.is_human_turn():
                    self.engine.make_move(*cell)

    def run(self):
        self.init_pygame()
        while self.running:
            self.handle_events()

            if not self.engine.game_over:
                if not self.engine.is_human_turn():
                    self.engine.play_ai_turn()

            self.draw_board()
            self.draw_pieces(self.engine.board)
            self.draw_status()
            pygame.display.flip()
            self.clock.tick(FPS)
        self.quit()

    def quit(self):
        pygame.quit()
