"""A small graphical Connect Four game built with Pygame."""

from __future__ import annotations

import argparse
import random

import pygame

from game_logic import (
    COLS,
    EMPTY,
    PLAYER_ONE,
    PLAYER_TWO,
    ROWS,
    Board,
    choose_ai_move,
    create_board,
    drop_piece,
    has_won,
    is_full,
)

CELL_SIZE = 92
MARGIN = 32
STATUS_HEIGHT = 92
WIDTH = COLS * CELL_SIZE + MARGIN * 2
HEIGHT = ROWS * CELL_SIZE + STATUS_HEIGHT + MARGIN * 2
BOARD_TOP = STATUS_HEIGHT + MARGIN

BACKGROUND = (18, 23, 35)
BOARD_BLUE = (36, 99, 235)
EMPTY_SLOT = (10, 15, 26)
PLAYER_COLORS = {
    PLAYER_ONE: (245, 75, 75),
    PLAYER_TWO: (250, 204, 21),
}
TEXT = (241, 245, 249)
MUTED_TEXT = (148, 163, 184)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Play Connect Four with Pygame.")
    parser.add_argument(
        "--mode",
        choices=("ai", "human"),
        default="ai",
        help="play against the computer or another person (default: ai)",
    )
    parser.add_argument(
        "--first",
        choices=("player1", "player2", "random"),
        default="random",
        help="choose who starts each game (default: random)",
    )
    return parser.parse_args()


def starting_player(first: str) -> int:
    if first == "player1":
        return PLAYER_ONE
    if first == "player2":
        return PLAYER_TWO
    return random.choice((PLAYER_ONE, PLAYER_TWO))


def column_from_position(position: tuple[int, int]) -> int | None:
    x, y = position
    if not (MARGIN <= x < WIDTH - MARGIN and BOARD_TOP <= y < HEIGHT - MARGIN):
        return None
    return (x - MARGIN) // CELL_SIZE


def status_message(current_player: int, mode: str, winner: int | None, draw: bool) -> str:
    if winner is not None:
        if mode == "ai" and winner == PLAYER_TWO:
            return "Computer wins!"
        return f"Player {winner} wins!"
    if draw:
        return "Draw!"
    if mode == "ai" and current_player == PLAYER_TWO:
        return "Computer is thinking..."
    return f"Player {current_player}'s turn"


def draw_scene(
    screen: pygame.Surface,
    board: Board,
    current_player: int,
    mode: str,
    winner: int | None,
    draw: bool,
) -> None:
    screen.fill(BACKGROUND)
    title_font = pygame.font.Font(None, 42)
    help_font = pygame.font.Font(None, 25)

    message = status_message(current_player, mode, winner, draw)
    title = title_font.render(message, True, TEXT)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 42)))

    help_text = "Click a column or press 1-7  |  R: restart  |  Esc: quit"
    help_surface = help_font.render(help_text, True, MUTED_TEXT)
    screen.blit(help_surface, help_surface.get_rect(center=(WIDTH // 2, 76)))

    board_rect = pygame.Rect(
        MARGIN,
        BOARD_TOP,
        COLS * CELL_SIZE,
        ROWS * CELL_SIZE,
    )
    pygame.draw.rect(screen, BOARD_BLUE, board_rect, border_radius=18)

    radius = CELL_SIZE // 2 - 10
    for row in range(ROWS):
        for column in range(COLS):
            center = (
                MARGIN + column * CELL_SIZE + CELL_SIZE // 2,
                BOARD_TOP + row * CELL_SIZE + CELL_SIZE // 2,
            )
            value = board[row][column]
            color = EMPTY_SLOT if value == EMPTY else PLAYER_COLORS[value]
            pygame.draw.circle(screen, color, center, radius)

    pygame.display.flip()


def main() -> None:
    args = parse_args()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect Four")
    clock = pygame.time.Clock()

    board = create_board()
    current_player = starting_player(args.first)
    winner: int | None = None
    draw = False
    running = True
    ai_move_at = pygame.time.get_ticks() + 500

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    board = create_board()
                    current_player = starting_player(args.first)
                    winner = None
                    draw = False
                    ai_move_at = pygame.time.get_ticks() + 500
                elif (
                    pygame.K_1 <= event.key <= pygame.K_7
                    and winner is None
                    and not draw
                    and (args.mode == "human" or current_player == PLAYER_ONE)
                ):
                    column = event.key - pygame.K_1
                    if drop_piece(board, column, current_player) is not None:
                        if has_won(board, current_player):
                            winner = current_player
                        elif is_full(board):
                            draw = True
                        else:
                            current_player = PLAYER_TWO if current_player == PLAYER_ONE else PLAYER_ONE
                            ai_move_at = pygame.time.get_ticks() + 450
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and winner is None
                and not draw
                and (args.mode == "human" or current_player == PLAYER_ONE)
            ):
                column = column_from_position(event.pos)
                if column is not None and drop_piece(board, column, current_player) is not None:
                    if has_won(board, current_player):
                        winner = current_player
                    elif is_full(board):
                        draw = True
                    else:
                        current_player = PLAYER_TWO if current_player == PLAYER_ONE else PLAYER_ONE
                        ai_move_at = pygame.time.get_ticks() + 450

        if (
            running
            and args.mode == "ai"
            and current_player == PLAYER_TWO
            and winner is None
            and not draw
            and pygame.time.get_ticks() >= ai_move_at
        ):
            column = choose_ai_move(board)
            if column is not None:
                drop_piece(board, column, PLAYER_TWO)
                if has_won(board, PLAYER_TWO):
                    winner = PLAYER_TWO
                elif is_full(board):
                    draw = True
                else:
                    current_player = PLAYER_ONE

        draw_scene(screen, board, current_player, args.mode, winner, draw)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
