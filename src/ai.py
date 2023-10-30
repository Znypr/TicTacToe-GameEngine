import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import pickle

from net import TicTacToeNet


# Define constants
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY_CELL = " "


def board_to_tensor(board):
    """Convert the board to a tensor representation."""
    tensor = []
    for row in board:
        for cell in row:
            if cell == "X":
                tensor.append(1.0)
            elif cell == "O":
                tensor.append(-1.0)
            else:
                tensor.append(0.0)
    return torch.tensor(tensor, dtype=torch.float32).unsqueeze(0)


def predict_best_move(model, board, player):
    tensor = board_to_tensor(board)
    with torch.no_grad():
        predictions = model(tensor)
    predictions = predictions.numpy().reshape(3, 3)

    # Get the coordinates of the highest value prediction for an empty cell
    while True:
        row, col = np.unravel_index(predictions.argmax(), predictions.shape)
        if board[row][col] == " ":
            return row, col
        else:
            predictions[row][
                col
            ] = -np.inf  # Set the chosen cell to negative infinity and re-loop


class TicTacToeAI:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.2):
        self.q_table = {}  # Q-table to store state-action values
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob

    def get_state_key(self, board):
        """Convert the board state to a unique string key for the Q-table."""
        return str(board)

    def choose_action(self, board):
        """Choose an action (row, col) based on the current state and Q-values."""
        # Create a copy of the board for exploring and exploiting
        board_copy = [row[:] for row in board]
        state_key = self.get_state_key(board_copy)

        # Explore (with probability exploration_prob) or exploit (with probability 1-exploration_prob)
        if random.uniform(0, 1) < self.exploration_prob:
            return self.random_action(board_copy)
        else:
            return self.best_action(board_copy)

    def random_action(self, board):
        """Choose a random empty cell (row, col) as an action."""
        empty_cells = [
            (r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY_CELL
        ]
        return random.choice(empty_cells)

    def best_action(self, board):
        """Choose the action with the highest Q-value for the current state."""
        state_key = self.get_state_key(board)
        if state_key in self.q_table:
            return max(self.q_table[state_key], key=self.q_table[state_key].get)
        else:
            return self.random_action(board)

    def update_q_table(self, state, action, reward, next_state):
        """Update the Q-table using the Q-learning algorithm."""
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {}

        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {}

        # Calculate the Q-value update
        if next_state_key in self.q_table and self.q_table[next_state_key]:
            max_next_q = max(self.q_table[next_state_key].values())
        else:
            max_next_q = 0  # If the game has ended

        current_q = self.q_table[state_key].get(action, 0)
        updated_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        self.q_table[state_key][action] = updated_q

    def train(self, episodes):
        # Load the Q-table from a file (before training)
        try:
            with open("q_table.pkl", "rb") as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            pass

        for _ in range(episodes):
            board = [[EMPTY_CELL] * 3 for _ in range(3)]
            current_player = PLAYER_X
            episode_history = []

            while True:
                action = self.choose_action(board)
                row, col = action
                board[row][col] = current_player

                if current_player == PLAYER_X:
                    next_player = PLAYER_O
                else:
                    next_player = PLAYER_X

                state_copy = [row[:] for row in board]
                episode_history.append((state_copy, action))

                game_over, winner = self.check_game_over(board)

                if game_over:
                    if winner == PLAYER_X:
                        self.update_q_values(episode_history, 1)
                    elif winner == PLAYER_O:
                        self.update_q_values(episode_history, -1)
                    else:
                        self.update_q_values(episode_history, 0)
                    break

                current_player = next_player

        # Save the Q-table to a file (after training)
        with open("q_table.pkl", "wb") as f:
            pickle.dump(self.q_table, f)

    def update_q_values(self, episode_history, final_reward):
        """Update Q-values based on the final reward and episode history."""
        for state, action in reversed(episode_history):
            # Assign rewards to previous actions based on the final outcome
            self.update_q_table(state, action, final_reward, state)
            final_reward = -final_reward  # Reverse rewards for the other player

    def check_game_over(self, board):
        """Check if the game is over and return the winner (if any)."""
        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != EMPTY_CELL:
                return True, board[i][0]  # Row win
            if board[0][i] == board[1][i] == board[2][i] != EMPTY_CELL:
                return True, board[0][i]  # Column win
        if board[0][0] == board[1][1] == board[2][2] != EMPTY_CELL:
            return True, board[0][0]  # Diagonal win
        if board[0][2] == board[1][1] == board[2][0] != EMPTY_CELL:
            return True, board[0][2]
            # Check for a draw
        if all(cell != EMPTY_CELL for row in board for cell in row):
            return True, None

        return False, None

    def play(self):
        """Play a game of Tic Tac Toe against the AI."""
        board = [[EMPTY_CELL] * 3 for _ in range(3)]
        current_player = PLAYER_X

        while True:
            self.display_board(board)

            if current_player == PLAYER_X:
                row, col = map(int, input("Enter your move (row col): ").split())
                if not self.is_valid_move(board, row, col):
                    print("Invalid move. Try again.")
                    continue
                board[row][col] = PLAYER_X
            else:
                print("AI's move:")
                board_copy = [
                    row[:] for row in board
                ]  # Create a copy of the board for AI
                row, col = self.choose_action(board_copy)
                board[row][col] = PLAYER_O

            game_over, winner = self.check_game_over(board)

            if game_over:
                self.display_board(board)
                if winner == PLAYER_X:
                    print("Congratulations! You win!")
                elif winner == PLAYER_O:
                    print("AI wins!")
                else:
                    print("It's a draw!")
                break

            current_player = PLAYER_X if current_player == PLAYER_O else PLAYER_O

    def display_board(self, board):
        """Display the Tic Tac Toe board."""
        print("-------------")
        for row in board:
            print("|", end=" ")
            for cell in row:
                print(cell, end=" | ")
            print("\n-------------")

    def is_valid_move(self, board, row, col):
        """Check if a move is valid (empty cell)."""
        if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == EMPTY_CELL:
            return True
        return False


if __name__ == "__main__":
    ai = TicTacToeAI()
    ai.train(episodes=100000)  # Train the AI (adjust the number of episodes as needed)
    ai.play()  # Play a game against the trained AI
