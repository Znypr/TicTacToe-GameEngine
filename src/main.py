import torch
from game import TicTacToe
from ai import predict_best_move
from net import TicTacToeNet


def main():
    game = TicTacToe()
    model = TicTacToeNet()
    model.load_state_dict(torch.load("../data/model.pth"))
    model.eval()

    while True:
        game.display_board()

        # Human player's move
        if game.current_player == "X":
            row, col = map(
                int,
                input(
                    f"Player {game.current_player}, enter your move (row col): "
                ).split(),
            )
            result = game.make_move(row, col)
        # AI's move
        else:
            row, col = predict_best_move(model, game.board, "O")
            print(f"AI chooses: {row} {col}")
            result = game.make_move(row, col)

        if result:
            game.display_board()
            print(result)
            if input("Play again? (y/n): ").lower() != "y":
                break
            game.reset_game()


if __name__ == "__main__":
    main()
