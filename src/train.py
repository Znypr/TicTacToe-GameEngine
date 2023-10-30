import torch
from net import TicTacToeNet

# Initialize the model
model = TicTacToeNet()

# Save the model's state_dict
torch.save(model.state_dict(), "../data/model.pth")
