import unittest

from game_logic import (
    PLAYER_ONE,
    PLAYER_TWO,
    available_row,
    choose_ai_move,
    create_board,
    drop_piece,
    has_won,
    is_full,
)


class GameLogicTests(unittest.TestCase):
    def test_piece_falls_to_lowest_available_row(self):
        board = create_board()
        self.assertEqual(drop_piece(board, 0, PLAYER_ONE), 5)
        self.assertEqual(available_row(board, 0), 4)

    def test_rejects_invalid_or_full_columns(self):
        board = create_board()
        self.assertIsNone(drop_piece(board, -1, PLAYER_ONE))
        self.assertIsNone(drop_piece(board, 7, PLAYER_ONE))
        for _ in range(6):
            drop_piece(board, 0, PLAYER_ONE)
        self.assertIsNone(drop_piece(board, 0, PLAYER_TWO))

    def test_detects_wins_in_every_direction(self):
        winning_cells = (
            ((5, 0), (5, 1), (5, 2), (5, 3)),
            ((2, 4), (3, 4), (4, 4), (5, 4)),
            ((2, 0), (3, 1), (4, 2), (5, 3)),
            ((5, 0), (4, 1), (3, 2), (2, 3)),
        )
        for cells in winning_cells:
            with self.subTest(cells=cells):
                board = create_board()
                for row, column in cells:
                    board[row][column] = PLAYER_ONE
                self.assertTrue(has_won(board, PLAYER_ONE))

    def test_detects_full_board(self):
        board = [[PLAYER_ONE] * 7 for _ in range(6)]
        self.assertTrue(is_full(board))

    def test_ai_takes_winning_move(self):
        board = create_board()
        for column in (0, 1, 2):
            drop_piece(board, column, PLAYER_TWO)
        self.assertEqual(choose_ai_move(board), 3)

    def test_ai_blocks_opponent(self):
        board = create_board()
        for column in (0, 1, 2):
            drop_piece(board, column, PLAYER_ONE)
        self.assertEqual(choose_ai_move(board), 3)

    def test_ai_prefers_center(self):
        self.assertEqual(choose_ai_move(create_board()), 3)

    def test_ai_returns_none_for_full_board(self):
        board = [[PLAYER_ONE] * 7 for _ in range(6)]
        self.assertIsNone(choose_ai_move(board))


if __name__ == "__main__":
    unittest.main()
