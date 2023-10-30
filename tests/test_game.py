from game import TicTacToe


def test_board_initialization():
    game = TicTacToe()
    for row in game.board:
        for cell in row:
            assert cell == " "


def test_valid_move():
    game = TicTacToe()
    result = game.make_move(1, 1)
    assert game.board[1][1] == "X"
    assert result is None


def test_invalid_move():
    game = TicTacToe()
    game.make_move(1, 1)
    result = game.make_move(1, 1)
    assert result == "Cell already occupied. Try again."


def test_win_conditions():
    game = TicTacToe()
    game.make_move(0, 0)
    game.make_move(1, 0)
    game.make_move(0, 1)
    game.make_move(1, 1)
    result = game.make_move(0, 2)
    assert result == "Player X wins!"


def test_draw_condition():
    game = TicTacToe()
    moves = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (1, 2), (2, 0), (2, 2), (2, 1)]
    for move in moves:
        game.make_move(*move)
    assert game.check_draw()


def test_switch_player():
    game = TicTacToe()
    assert game.current_player == "X"
    game.switch_player()
    assert game.current_player == "O"
