import sys
import time

import pygame

import tictactoe as ttt


pygame.init()

WIDTH, HEIGHT = 960, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

FONT_PATH = "OpenSans-Regular.ttf"
font_tiny = pygame.font.Font(FONT_PATH, 14)
font_small = pygame.font.Font(FONT_PATH, 18)
font_body = pygame.font.Font(FONT_PATH, 24)
font_title = pygame.font.Font(FONT_PATH, 42)
font_hero = pygame.font.Font(FONT_PATH, 58)
font_move = pygame.font.Font(FONT_PATH, 74)

BACKGROUND = (11, 16, 29)
PANEL = (20, 28, 47)
PANEL_LIGHT = (28, 38, 62)
GRID = (65, 82, 116)
WHITE = (239, 244, 255)
MUTED = (137, 153, 183)
CYAN = (73, 219, 224)
PINK = (255, 104, 170)
GOLD = (255, 202, 92)
SHADOW = (5, 8, 16)


def draw_text(text, font, color, position, center=False):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = position
    else:
        rect.topleft = position
    screen.blit(surface, rect)
    return rect


def rounded_panel(rect, color=PANEL, radius=18, shadow=True):
    if shadow:
        shadow_rect = rect.move(0, 8)
        pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=radius)
    pygame.draw.rect(screen, color, rect, border_radius=radius)


def draw_background():
    screen.fill(BACKGROUND)
    pygame.draw.circle(screen, (19, 53, 70), (80, 80), 260)
    pygame.draw.circle(screen, (55, 24, 61), (WIDTH - 30, HEIGHT - 40), 300)
    pygame.draw.circle(screen, (16, 31, 57), (WIDTH // 2, HEIGHT // 2), 320)


def draw_header():
    draw_text("TIC-TAC-TOE", font_small, CYAN, (48, 34))


def draw_button(rect, label, accent, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    color = (37, 51, 79) if hovered else PANEL
    rounded_panel(rect, color, radius=14)
    pygame.draw.rect(screen, accent, rect, width=2, border_radius=14)
    draw_text(label, font_body, WHITE, rect.center, center=True)
    return hovered


def draw_start_screen(mouse_pos):
    draw_header()
    draw_text("Choose your side.", font_hero, WHITE, (WIDTH // 2, 200), center=True)

    card_width = 330
    card_height = 152
    left = pygame.Rect(118, 362, card_width, card_height)
    right = pygame.Rect(WIDTH - 118 - card_width, 362, card_width, card_height)

    for rect, mark, subtitle, accent in (
        (left, "X", "You move first", CYAN),
        (right, "O", "AI opens the tree", PINK),
    ):
        hovered = rect.collidepoint(mouse_pos)
        rounded_panel(rect, (32, 45, 70) if hovered else PANEL_LIGHT, radius=18)
        pygame.draw.rect(screen, accent, rect, width=2, border_radius=18)
        draw_text(mark, font_hero, accent, (rect.x + 34, rect.y + 25))
        draw_text(f"PLAY AS {mark}", font_body, WHITE, (rect.x + 118, rect.y + 38))
        draw_text(subtitle, font_small, MUTED, (rect.x + 118, rect.y + 82))
    draw_text("Click to begin", font_tiny, MUTED, (WIDTH // 2, 570), center=True)

    return left, right


def draw_status_panel(user, player, game_over, winner):
    panel = pygame.Rect(48, 108, WIDTH - 96, 92)
    rounded_panel(panel, PANEL, radius=18)
    pygame.draw.rect(screen, GRID, panel, width=1, border_radius=18)

    if game_over:
        if winner is None:
            title, detail, accent = "GAME COMPLETE", "A hard-fought draw.", GOLD
        elif winner == user:
            title, detail, accent = "YOU WIN", "Your strategy beat the search.", CYAN
        else:
            title, detail, accent = "AI WINS", "The search found a winning line.", PINK
    elif user == player:
        title, detail, accent = "YOUR TURN", f"Place your {user}.", CYAN if user == ttt.X else PINK
    else:
        title, detail, accent = "COMPUTER THINKING", "Evaluating possible futures...", PINK

    pygame.draw.circle(screen, accent, (78, 154), 10)
    draw_text(title, font_body, WHITE, (104, 128))
    draw_text(detail, font_small, MUTED, (104, 163))
    draw_text(f"YOU  {user}", font_small, accent, (WIDTH - 220, 130))
    draw_text(f"TURN  {player}", font_small, MUTED, (WIDTH - 220, 163))


def draw_board(board, mouse_pos):
    board_rect = pygame.Rect(255, 238, 450, 450)
    rounded_panel(board_rect.inflate(24, 24), PANEL, radius=26)
    tile_size = 134
    gap = 12
    origin_x, origin_y = 276, 259
    tiles = []

    for i in range(3):
        row = []
        for j in range(3):
            rect = pygame.Rect(
                origin_x + j * (tile_size + gap),
                origin_y + i * (tile_size + gap),
                tile_size,
                tile_size,
            )
            row.append(rect)
            hovered = rect.collidepoint(mouse_pos) and board[i][j] == ttt.EMPTY
            color = (35, 51, 79) if hovered else PANEL_LIGHT
            pygame.draw.rect(screen, color, rect, border_radius=16)
            pygame.draw.rect(screen, GRID, rect, width=2, border_radius=16)

            mark = board[i][j]
            if mark != ttt.EMPTY:
                accent = CYAN if mark == ttt.X else PINK
                draw_text(mark, font_move, accent, rect.center, center=True)
        tiles.append(row)
    return tiles


def draw_game_screen(board, user, mouse_pos):
    draw_header()
    game_over = ttt.terminal(board)
    player = ttt.player(board)
    winner = ttt.winner(board)
    draw_status_panel(user, player, game_over, winner)
    tiles = draw_board(board, mouse_pos)

    if game_over:
        button = pygame.Rect(350, 638, 260, 48)
        draw_button(button, "PLAY AGAIN", CYAN, mouse_pos)
        return tiles, game_over, player, button

    draw_text("THE BOARD IS THE STATE", font_tiny, MUTED, (WIDTH // 2, 692), center=True)
    return tiles, game_over, player, None


user = None
board = ttt.initial_state()
ai_turn = False

while True:
    mouse_pos = pygame.mouse.get_pos()
    click_position = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_position = event.pos

    draw_background()

    if user is None:
        play_x_button, play_o_button = draw_start_screen(mouse_pos)
        if click_position is not None:
            if play_x_button.collidepoint(click_position):
                time.sleep(0.15)
                user = ttt.X
            elif play_o_button.collidepoint(click_position):
                time.sleep(0.15)
                user = ttt.O
    else:
        tiles, game_over, player, again_button = draw_game_screen(
            board, user, mouse_pos
        )

        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.35)
                board = ttt.result(board, ttt.minimax(board))
                ai_turn = False
            else:
                ai_turn = True

        if click_position is not None and user == player and not game_over:
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(
                        click_position
                    ):
                        board = ttt.result(board, (i, j))

        if again_button is not None and click_position is not None:
            if again_button.collidepoint(click_position):
                time.sleep(0.15)
                user = None
                board = ttt.initial_state()
                ai_turn = False

    pygame.display.flip()
    clock.tick(60)
