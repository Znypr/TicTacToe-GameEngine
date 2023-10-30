from utils import board_to_string, string_to_board, is_valid_move, get_empty_cells


def test_board_string_conversion():
    board = [["X", "O", " "], [" ", "X", "O"], ["O", " ", "X"]]
    board_str = board_to_string(board)
    assert board_str == "X|O| \n-----\n |X|O\n-----\nO| |X"
    assert string_to_board(board_str) == board


def test_valid_move_check():
    board = [["X", "O", " "], [" ", "X", "O"], ["O", " ", "X"]]
    assert is_valid_move(board, 0, 2)
    assert not is_valid_move(board, 0, 0)


def test_get_empty_cells():
    board = [["X", "O", " "], [" ", "X", "O"], ["O", " ", "X"]]
    empty_cells = get_empty_cells(board)
    assert (0, 2) in empty_cells
    assert (1, 0) in empty_cells
    assert len(empty_cells) == 3
