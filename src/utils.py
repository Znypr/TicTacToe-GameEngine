def board_to_string(board):
    """Convert the board matrix to a string representation."""
    return "\n".join(["|".join(row) for row in board])


def string_to_board(board_str):
    """Convert a string representation of the board back to a matrix."""
    return [list(row) for row in board_str.split("\n")]


def save_board_to_file(board, filename):
    """Save the board to a file."""
    with open(filename, "w") as f:
        f.write(board_to_string(board))


def load_board_from_file(filename):
    """Load the board from a file."""
    with open(filename, "r") as f:
        return string_to_board(f.read())


def is_valid_move(board, row, col):
    """Check if a move is valid (i.e., cell is empty)."""
    return board[row][col] == " "


def get_empty_cells(board):
    """Return a list of coordinates for all empty cells."""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]


def copy_board(board):
    """Return a deep copy of the board."""
    return [row.copy() for row in board]
