import torch
from torch import Tensor
import torch.nn as nn

class NNModel(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, num_layers: int = 2) -> None:
        super(NNModel, self).__init__()
        
        # LSTM for sequence learning
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        
        # Output layers
        self.time_fc = nn.Linear(hidden_size, 1)  # Predict the time difference
        self.action_fc = nn.Linear(hidden_size, 2)  # Predict the action (on/off)
        
    def forward(self, x: Tensor) -> tuple[Tensor, Tensor]:
        # Pass the input through the LSTM
        lstm_out, _ = self.lstm(x)
        
        # Use the last output from the LSTM for predictions
        lstm_out_last = lstm_out[:, -1, :]
        
        # Predict time difference (continuous output)
        time_diff: Tensor = self.time_fc(lstm_out_last)
        
        # Predict action (classification output)
        action_logits: Tensor = self.action_fc(lstm_out_last)
        
        return time_diff, action_logits