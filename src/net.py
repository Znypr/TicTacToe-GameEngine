import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


class TicTacToeNet(nn.Module):
    def __init__(self):
        super(TicTacToeNet, self).__init__()
        self.fc1 = nn.Linear(9, 128)  # 3x3 board flattened
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 9)  # 9 possible moves

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x
