import torch
from ai import TicTacToeNet, board_to_tensor, predict_best_move


def test_forward_pass():
    model = TicTacToeNet()
    board = [[" " for _ in range(3)] for _ in range(3)]
    tensor = board_to_tensor(board)
    output = model(tensor)
    assert output.shape == (1, 9)


def test_board_to_tensor_conversion():
    board = [["X", "O", " "], [" ", "X", "O"], ["O", " ", "X"]]
    tensor = board_to_tensor(board)
    expected_tensor = torch.tensor([[1.0, -1.0, 0.0, 0.0, 1.0, -1.0, -1.0, 0.0, 1.0]])
    assert torch.equal(tensor, expected_tensor)


def test_predict_best_move():
    model = TicTacToeNet()
    board = [["X", "O", " "], [" ", "X", "O"], ["O", " ", "X"]]
    row, col = predict_best_move(model, board, "X")
    assert board[row][col] == " "
