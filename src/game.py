class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def display_board(self):
        for row in self.board:
            print("|".join(row))
            print("-" * 5)

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            if self.check_win():
                return f"Player {self.current_player} wins!"
            elif self.check_draw():
                return "It's a draw!"
            self.switch_player()
            return None
        else:
            return "Cell already occupied. Try again."

    def check_win(self):
        # Check rows, columns, and diagonals
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":  # Rows
                return True
            if (
                self.board[0][i] == self.board[1][i] == self.board[2][i] != " "
            ):  # Columns
                return True
        if (
            self.board[0][0] == self.board[1][1] == self.board[2][2] != " "
        ):  # Diagonal from top-left to bottom-right
            return True
        if (
            self.board[0][2] == self.board[1][1] == self.board[2][0] != " "
        ):  # Diagonal from top-right to bottom-left
            return True
        return False

    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == " ":
                    return False
        return True

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"


# Example usage:
if __name__ == "__main__":
    game = TicTacToe()
    while True:
        game.display_board()
        row, col = map(
            int,
            input(f"Player {game.current_player}, enter your move (row col): ").split(),
        )
        result = game.make_move(row, col)
        if result:
            game.display_board()
            print(result)
            if input("Play again? (y/n): ").lower() != "y":
                break
            game.reset_game()
