import torch
import torch.nn as nn
import torch.nn.functional as F

class NNModel(nn.Module):
    def __init__(self, input_size):
        super(NNModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 2)  # Output layer with 2 neurons

    def forward(self, x):
        x.float()
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        time_to_turn_on = torch.sigmoid(x[:, 0])  #Scale between 0 and 1
        duration = torch.sigmoid(x[:, 1]) # Scale between 0 and 1
        return time_to_turn_on.float(), duration.float()