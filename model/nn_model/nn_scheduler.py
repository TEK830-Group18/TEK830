from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset
from torch.utils.data import DataLoader, Subset
import torch
import torch.optim as optim
import torch.nn as nn
from typing import List
from model.events.lamp_event import LampEvent
from model.nn_model.nn_model import NNModel
from model.schedule import Schedule
from model.scheduler import Scheduler
from model.nn_model.lamp_event_dataset import LampEventDataset

class NNScheduler(Scheduler):
    def __init__(self):
        super().__init__()

    def create_schedule(self, user_actions: List[LampEvent]) -> Schedule:
        # Prepare the dataset for training
        dataset = LampEventDataset(user_actions)
        
        # Split the dataset into training and validation sets
        train_indices, val_indices = train_test_split(list(range(len(dataset))), test_size=0.2, random_state=42)
        train_dataset = Subset(dataset, train_indices)
        val_dataset = Subset(dataset, val_indices)
        
        # Train the model
        model = self.train_model(train_dataset)
        
        # Evaluate the model
        self.evaluate_model(model, val_dataset)

        return Schedule(events=user_actions)
    
    def train_model(self, train_dataset: Dataset) -> NNModel:
        # Hyperparameters
        input_size = 3  # Example: timestamp, lamp id, previous action
        hidden_size = 64
        num_epochs = 20
        learning_rate = 0.001

        # Initialize dataloader and model
        dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        model = NNModel(input_size, hidden_size)
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        # Loss functions
        time_loss_fn = nn.MSELoss()  # Regression loss for time difference
        action_loss_fn = nn.CrossEntropyLoss()  # Classification loss for action

        # Training loop
        for epoch in range(num_epochs):
            for sequences, time_diffs, actions in dataloader:
                # Forward pass
                predicted_time_diff, action_logits = model(sequences.float())
                
                # Compute losses
                time_loss = time_loss_fn(predicted_time_diff, time_diffs.float())
                action_loss = action_loss_fn(action_logits, actions.squeeze().long())
                
                # Total loss is the sum of time and action losses
                total_loss = time_loss + action_loss

                # Backward pass and optimization
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

        return model

    def evaluate_model(self, model: NNModel, val_dataset: Dataset):
        # Initialize dataloader
        dataloader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        
        # Evaluation metrics
        total_time_loss = 0.0
        total_action_correct = 0
        total_samples = 0
        
        # Loss functions
        time_loss_fn = nn.MSELoss()  # Regression loss for time difference
        action_loss_fn = nn.CrossEntropyLoss()  # Classification loss for action

        # Evaluation loop
        model.eval()
        with torch.no_grad():
            for sequences, time_diffs, actions in dataloader:
                # Forward pass
                predicted_time_diff, action_logits = model(sequences.float())
                
                # Compute losses
                time_loss = time_loss_fn(predicted_time_diff, time_diffs.float())
                total_time_loss += time_loss.item() * sequences.size(0)
                
                # Compute accuracy for action prediction
                _, predicted_actions = torch.max(action_logits, 1)
                total_action_correct += (predicted_actions == actions.squeeze().long()).sum().item()
                total_samples += sequences.size(0)
        
        # Calculate average time loss and action accuracy
        avg_time_loss = total_time_loss / total_samples
        action_accuracy = total_action_correct / total_samples
        
        print(f'Validation Time Loss: {avg_time_loss:.4f}')
        print(f'Validation Action Accuracy: {action_accuracy:.4f}')