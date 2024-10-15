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

from model.nn_model.lstm_model import LSTMModel

class NNScheduler(Scheduler):
    def __init__(self):
        super().__init__()

    def createSchedule(self, user_actions: List[LampEvent]) -> Schedule:
        print("Preparing data...")
        dataset = LampEventDataset(user_actions)
        
        train_indices, val_indices = train_test_split(list(range(len(dataset))), test_size=0.2, random_state=42)
        train_dataset = Subset(dataset, train_indices)
        val_dataset = Subset(dataset, val_indices)
        
        print("Training model...")
        model = self.train_model(train_dataset)
        
        print("Evaluating model...")
        self.evaluate_model(model, val_dataset)
        
        print("Generating schedule...")
        return self.generate_24_hour_schedule(model, dataset)
    
    def train_model(self, train_dataset: Dataset) -> LSTMModel:
        input_size = 2  # Example: time of day, lamp id
        hidden_size = 64
        num_layers = 2
        output_size = 2  # Example: ON/OFF actions
        num_epochs = 20
        learning_rate = 0.001
        
        dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True)
        model = LSTMModel(input_size, hidden_size, num_layers, output_size)
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        criterion = nn.CrossEntropyLoss()
        
        progress = progressbar.ProgressBar(num_epochs)
        for epoch in progress(range(num_epochs)):
            for sequences, actions in dataloader:
                sequences = sequences.unsqueeze(1)  
                actions = actions.long().squeeze()
                
                outputs = model(sequences.float())
                loss = criterion(outputs, actions)
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        
        return model

    def evaluate_model(self, model: LSTMModel, val_dataset: Dataset):
        dataloader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        
        total_correct = 0
        total_samples = 0
        
        model.eval()
        with torch.no_grad():
            for sequences, actions in dataloader:
                sequences = sequences.unsqueeze(1)  # Add batch dimension
                actions = actions.long()
                
                outputs = model(sequences.float())
                _, predicted = torch.max(outputs, 1)
                total_correct += (predicted == actions).sum().item()
                total_samples += actions.size(0)
        
        accuracy = total_correct / total_samples
        print(f'Validation Accuracy: {accuracy:.4f}')
        
    def generate_24_hour_schedule(self, model: LSTMModel, dataset: LampEventDataset) -> Schedule:
        model.eval()
        schedule_events = []
        
        with torch.no_grad():
            for lamp_id in dataset.lamp_id_to_int.keys():
                previous_action = None
                for minute in range(1440):
                    time_of_day_tensor = torch.tensor([minute], dtype=torch.float32)
                    lamp_id_tensor = torch.tensor([dataset.lamp_id_to_int[lamp_id]], dtype=torch.float32)
                    sequence_tensor = torch.cat((time_of_day_tensor, lamp_id_tensor), dim=0).unsqueeze(0).unsqueeze(0)
                    
                    outputs = model(sequence_tensor)
                    _, predicted_action = torch.max(outputs, 1)
                    action = LampAction.ON if predicted_action.item() == 1 else LampAction.OFF
                    
                    if previous_action is None or action != previous_action:
                        timestamp = datetime.today().replace(hour=minute // 60, minute=minute % 60, second=0, microsecond=0)
                        schedule_events.append(LampEvent(lamp=lamp_id, timestamp=timestamp, action=action))
                        previous_action = action
        
        return Schedule(events=schedule_events)