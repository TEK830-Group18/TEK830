import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torch.optim import Optimizer
from model.nn_model.time_duration_predictor import TimeDurationPredictor

class LinearModel(TimeDurationPredictor):
    class __NNModel(nn.Module):
        def __init__(self, input_size):
            super().__init__()
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

    def __init__(self, input_size):
        self.model = self.__NNModel(input_size)

    def predict(self, X) -> tuple[Tensor, Tensor]:
        self.model.eval()
        with torch.no_grad():
            return self.model(X)
    
    def train(self, X: Tensor, y: Tensor, criterion: nn.Module, optimizer: Optimizer, epochs: int) -> None:
        # Set the model to training mode
        self.model.train()
        for epoch in range(epochs):
            # Forward pass
            time_to_turn_on, duration = self.model(X.float())
            
            # Squeeze the extra dimension out of y_train
            y = y.squeeze(1)
            
            # Ensure the target tensors are 1D
            time_targets = y[:, 0].float()
            duration_targets = y[:, 1].float()
            
            # Compute loss for each output
            loss_time = criterion(time_to_turn_on, time_targets)
            loss_duration = criterion(duration, duration_targets)
            
            # Combine losses
            loss = loss_time + loss_duration
            
            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')

    def evaluate(self, X: Tensor, y: Tensor) -> dict[str, float]:
        # Predict values for X
        predicted_start, predicted_duration = self.predict(X)
        
        y  = y.squeeze(1)

        # Separate actual start time and duration from y
        true_start = y[:, 0]
        true_duration = y[:, 1]
        
        # Compute MAE for start time and duration
        start_mae = float(torch.mean(torch.abs(predicted_start - true_start)).item())
        duration_mae = float(torch.mean(torch.abs(predicted_duration - true_duration)).item())
        
        # Compute MSE for start time and duration
        start_mse = float(torch.mean((predicted_start - true_start) ** 2).item())
        duration_mse = float(torch.mean((predicted_duration - true_duration) ** 2).item())
        
        # Compute MAPE for start time and duration
        start_mape = float((torch.mean(torch.abs((true_start - predicted_start) / true_start)) * 100).item())
        duration_mape = float((torch.mean(torch.abs((true_duration - predicted_duration) / true_duration)) * 100).item())

        # Output metrics
        metrics = {
            'start_mae': start_mae,
            'duration_mae': duration_mae,
            'start_mse': start_mse,
            'duration_mse': duration_mse,
            'start_mape': start_mape,
            'duration_mape': duration_mape
        }

        return metrics
    
    def parameters(self):
        return self.model.parameters()
