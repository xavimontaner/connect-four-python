"""Pure Connect Four game rules and computer-player decisions."""

from __future__ import annotations

import random
from collections.abc import Callable

ROWS = 6
COLS = 7
EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2

Board = list[list[int]]


def create_board() -> Board:
    """Return an empty 6x7 Connect Four board."""
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def available_row(board: Board, column: int) -> int | None:
    """Return the lowest free row in ``column``, or ``None`` when full."""
    if not 0 <= column < COLS:
        return None

    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == EMPTY:
            return row
    return None


def available_columns(board: Board) -> list[int]:
    """Return every column that can accept another piece."""
    return [column for column in range(COLS) if board[0][column] == EMPTY]


def drop_piece(board: Board, column: int, player: int) -> int | None:
    """Place a piece and return its row, or ``None`` for an invalid move."""
    row = available_row(board, column)
    if row is None:
        return None

    board[row][column] = player
    return row


def is_full(board: Board) -> bool:
    """Return whether the board has no valid moves remaining."""
    return not available_columns(board)


def has_won(board: Board, player: int) -> bool:
    """Return whether ``player`` has four connected pieces."""
    for row in range(ROWS):
        for column in range(COLS - 3):
            if all(board[row][column + offset] == player for offset in range(4)):
                return True

    for row in range(ROWS - 3):
        for column in range(COLS):
            if all(board[row + offset][column] == player for offset in range(4)):
                return True

    for row in range(ROWS - 3):
        for column in range(COLS - 3):
            if all(
                board[row + offset][column + offset] == player
                for offset in range(4)
            ):
                return True

    for row in range(3, ROWS):
        for column in range(COLS - 3):
            if all(
                board[row - offset][column + offset] == player
                for offset in range(4)
            ):
                return True

    return False


def choose_ai_move(
    board: Board,
    ai_player: int = PLAYER_TWO,
    opponent: int = PLAYER_ONE,
    chooser: Callable[[list[int]], int] = random.choice,
) -> int | None:
    """Choose a winning, blocking, central, or random valid move."""
    columns = available_columns(board)
    if not columns:
        return None

    for player in (ai_player, opponent):
        for column in columns:
            row = drop_piece(board, column, player)
            assert row is not None
            wins = has_won(board, player)
            board[row][column] = EMPTY
            if wins:
                return column

    center = COLS // 2
    if center in columns:
        return center

    return chooser(columns)
