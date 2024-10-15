import torch.nn as nn
import torch.nn.functional as F

class NNModel(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(NNModel, self).__init__()
        # self.fc1 = nn.Linear(input_size, hidden_size)
        # self.fc2 = nn.Linear(hidden_size, 2)  # Output layer for binary classification (on/off)
        self.fc1 = nn.Linear(input_size, 64)
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.hiddenToAction = nn.Linear(hidden_size, 2)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        out = self.fc2(x)
        return out
    