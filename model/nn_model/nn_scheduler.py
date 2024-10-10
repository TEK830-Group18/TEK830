from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Subset
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import Dataset
from typing import List
from model.events.lamp_action import LampAction
from model.events.lamp_event import LampEvent
from model.nn_model.nn_model import NNModel
from model.schedule import Schedule
from model.scheduler import Scheduler
from model.nn_model.lamp_event_dataset import LampEventDataset
from progressbar import progressbar

class NNScheduler(Scheduler):
    def __init__(self):
        super().__init__()

    def create_schedule(self, user_actions: List[LampEvent]) -> Schedule:
        # Prepare the dataset for training
        print("Preparing data...")
        dataset = LampEventDataset(user_actions)
        
        # Split the dataset into training and validation sets
        train_indices, val_indices = train_test_split(list(range(len(dataset))), test_size=0.2, random_state=42)
        train_dataset = Subset(dataset, train_indices)
        val_dataset = Subset(dataset, val_indices)
        
        # Train the model
        model = self.train_model(train_dataset)
        
        # Evaluate the model
        self.evaluate_model(model, val_dataset)

        return self.generate_24_hour_schedule(model, dataset)
    
    def train_model(self, train_dataset: Dataset) -> NNModel:
        # Hyperparameters
        input_size = 2  # Example: time of day, lamp id
        hidden_size = 64
        num_epochs = 20
        learning_rate = 0.001

        # Initialize dataloader and model
        dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True)
        model = NNModel(input_size, hidden_size)
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        print("Training model...")
        
        # Loss function
        action_loss_fn = nn.CrossEntropyLoss() 

        # Training loop
        progress = progressbar.ProgressBar(num_epochs)
        for epoch in progress(range(num_epochs)):
            for sequences, actions in dataloader:
                # Forward pass
                action_logits = model(sequences.float())
                
                # Compute losses
                action_loss = action_loss_fn(action_logits, actions.squeeze().long())
                
                # Backward pass and optimization
                optimizer.zero_grad()
                action_loss.backward()
                optimizer.step()

        return model

    def evaluate_model(self, model: NNModel, val_dataset: Dataset):
        print("Evaluating model...")
        # Initialize dataloader
        dataloader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        
        # Evaluation metrics
        total_action_correct = 0
        total_samples = 0
        
        # Evaluation loop
        model.eval()
        with torch.no_grad():
            for sequences, actions in dataloader:
                # Forward pass
                action_logits = model(sequences.float())
                
                # Compute accuracy for action prediction
                _, predicted_actions = torch.max(action_logits, 1)
                total_action_correct += (predicted_actions == actions.squeeze().long()).sum().item()
                total_samples += sequences.size(0)
        
        # Calculate action accuracy
        action_accuracy = total_action_correct / total_samples
        
        print(f'Validation Action Accuracy: {action_accuracy:.4f}')
        
    def generate_24_hour_schedule(self, model: NNModel, dataset: LampEventDataset) -> Schedule:
        # Generate actions for 24 hour period
        model.eval()
        schedule_events = []

        with torch.no_grad():
            for lamp_id in dataset.lamp_id_to_int.keys():
                previous_action = None
                for minute in range(1440):  # 1440 minutes in a day
                    time_of_day_tensor = torch.tensor([minute], dtype=torch.float32)
                    lamp_id_tensor = torch.tensor([dataset.lamp_id_to_int[lamp_id]], dtype=torch.float32)
                    sequence_tensor = torch.cat((time_of_day_tensor, lamp_id_tensor), dim=0).unsqueeze(0)  # Shape (1, 2)
                    
                    action_logits = model(sequence_tensor)
                    _, predicted_action = torch.max(action_logits, 1)
                    action = LampAction.ON if predicted_action.item() == 1 else LampAction.OFF
                    
                    if previous_action is None or action != previous_action:
                        timestamp = datetime.today().replace(hour=minute // 60, minute=minute % 60, second=0, microsecond=0)
                        schedule_events.append(LampEvent(lamp=lamp_id, timestamp=timestamp, action=action))
                        previous_action = action

        print(len(schedule_events))
        return Schedule(events=schedule_events)