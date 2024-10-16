# from datetime import datetime, timedelta
# from sklearn.model_selection import train_test_split
# from torch.utils.data import DataLoader, Subset
# import torch
# import torch.optim as optim
# import torch.nn as nn
# from torch.utils.data import Dataset
# from typing import List
# from model.events.lamp_action import LampAction
# from model.events.lamp_event import LampEvent
# from model.nn_model.nn_model import NNModel
# from model.schedule import Schedule
# from model.scheduler import Scheduler
# from model.nn_model.lamp_event_dataset import LampEventDataset
# from progressbar import progressbar

# from model.nn_model.lstm_model import LSTMModel

# class NNScheduler(Scheduler):
#     def __init__(self):
#         super().__init__()

#     def createSchedule(self, user_actions: List[LampEvent]) -> Schedule:
#         print("Preparing data...")
#         dataset = LampEventDataset(user_actions)
        
#         train_indices, val_indices = train_test_split(list(range(len(dataset))), test_size=0.2, random_state=42)
#         train_dataset = Subset(dataset, train_indices)
#         val_dataset = Subset(dataset, val_indices)
        
#         print("Training model...")
#         model = self.train_model(train_dataset)
        
#         # print("Evaluating model...")
#         # self.evaluate_model(model, val_dataset)
        
#         print("Generating schedule...")
#         return self.generate_24_hour_schedule(model, dataset)
    
#     def train_model(self, train_dataset: Dataset) -> LSTMModel:
#         input_size = 2  # Example: time of day, lamp id
#         hidden_size = 16
#         num_layers = 2
#         output_size = 2  # Example: ON/OFF actions
#         num_epochs = 20
#         learning_rate = 0.001
        
#         dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True)
#         model = LSTMModel(input_size, hidden_size, num_layers, output_size)
#         optimizer = optim.Adam(model.parameters(), lr=learning_rate)
#         criterion = nn.CrossEntropyLoss()
        
#         progress = progressbar.ProgressBar(num_epochs)
#         for epoch in progress(range(num_epochs)):
#             for sequences, actions in dataloader:
#                 sequences = sequences.unsqueeze(1)  
#                 actions = actions.long().squeeze()
                
#                 outputs = model(sequences.float())
#                 loss = criterion(outputs, actions)
                
#                 optimizer.zero_grad()
#                 loss.backward()
#                 optimizer.step()
        
#         return model

#     def evaluate_model(self, model: LSTMModel, val_dataset: Dataset):
#         dataloader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        
#         total_correct = 0
#         total_samples = 0
        
#         model.eval()
#         with torch.no_grad():
#             for sequences, actions in dataloader:
#                 sequences = sequences.unsqueeze(1)  # Add batch dimension
#                 actions = actions.long()
                
#                 outputs = model(sequences.float())
#                 _, predicted = torch.max(outputs, 1)
#                 total_correct += (predicted == actions).sum().item()
#                 total_samples += actions.size(0)
        
#         accuracy = total_correct / total_samples
#         print(f'Validation Accuracy: {accuracy:.4f}')
        
#     def generate_24_hour_schedule(self, model: LSTMModel, dataset: LampEventDataset) -> Schedule:
#         model.eval()
#         schedule_events = []
        
#         with torch.no_grad():
#             for lamp_id in dataset.lamp_id_to_int.keys():
#                 previous_action = None
#                 for minute in range(1440):
#                     time_of_day_tensor = torch.tensor([minute], dtype=torch.float32)
#                     lamp_id_tensor = torch.tensor([dataset.lamp_id_to_int[lamp_id]], dtype=torch.float32)
#                     sequence_tensor = torch.cat((time_of_day_tensor, lamp_id_tensor), dim=0).unsqueeze(0).unsqueeze(0)
                    
#                     outputs = model(sequence_tensor)
#                     _, predicted_action = torch.max(outputs, 1)
#                     item  = predicted_action.item()
#                     action = LampAction.ON if item > 0.5 else LampAction.OFF
                    
#                     if previous_action is None or action != previous_action:
#                         timestamp = datetime.today().replace(hour=minute // 60, minute=minute % 60, second=0, microsecond=0)
#                         schedule_events.append(LampEvent(lamp=lamp_id, timestamp=timestamp, action=action))
#                         previous_action = action
#         schedule_events.sort(key=lambda x: x.timestamp.hour * 60 + x.timestamp.minute)
#         return Schedule(events=schedule_events)


from datetime import datetime, timedelta
from typing import List

import pandas as pd
from pandas import DataFrame, Series
from sklearn.model_selection import train_test_split
import torch
from model.events.lamp_action import LampAction
from model.events.lamp_event import LampEvent
from model.nn_model.nn_model import NNModel
from model.schedule import Schedule
from model.scheduler import Scheduler


class NNScheduler(Scheduler):
    def __init__(self):
        super().__init__()

    def createSchedule(self, user_actions: List[LampEvent]) -> Schedule:
        # Prepare the data
        features, target, lamp_names = self.format_data(user_actions)
        X_train, X_test, y_train, y_test = self.split_data(features, target)
        X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor = self.to_tensors(X_train, X_test, y_train, y_test)

        # Initialize the model
        input_size = X_train_tensor.shape[1] # The number of features
        model: NNModel = NNModel(input_size)

        # Loss function and optimizer
        criterion = torch.nn.BCELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        # Train the model
        self.train_model(model, X_train_tensor, y_train_tensor, criterion, optimizer, num_epochs=20)

        # Evaluate the model
        self.evaluate_model(model, X_test_tensor, y_test_tensor)

        # Generate a 24-hour schedule
        # lamp_names = features['lamp'].unique()
        timestamps = self.generate_24_hour_minute_timestamps(datetime.now())
        schedule = self.create_24_hour_schedule(lamp_names, timestamps, model, features.columns.tolist())

        return schedule

    def format_data(self, user_actions: List[LampEvent]) -> tuple[DataFrame, Series, list[str]]:
        data = self.extract_features(user_actions)

        # Create a pandas DataFrame
        df = DataFrame(data)

        # Get the unique lamp names
        original_lamp_names = df['lamp'].unique().tolist()
        
        # One-hot encode the lamp field
        df = pd.get_dummies(df, columns=['lamp'], prefix='lamp', dtype=float)

        features = df.drop('action', axis=1)
        target = df['action']
        print(features)
        return features, target, original_lamp_names
    
    def split_data(self, features: DataFrame, target: Series) -> tuple[DataFrame, DataFrame, Series, Series]:
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    
    def to_tensors(self, X_train, X_test, y_train, y_test) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
        y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).unsqueeze(1)  # Convert to (N, 1) shape
        X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
        y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).unsqueeze(1)  # Convert to (N, 1) shape
        return X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor
    
    def extract_features(self, events: List[LampEvent]) -> List[dict]:
        # Extract features from the events
        data = []
        for event in events:
            # Extract timestamp features
            hour = event.timestamp.hour
            day_of_week = event.timestamp.weekday()
            month = event.timestamp.month
            is_weekend = 1 if day_of_week >= 5 else 0
            
            # Encode the action (on=1, off=0)
            action = 1 if event.action == LampAction.ON else 0
            
            # Collect the data (you can extend this to include more features if necessary)
            data.append({
                'hour': hour,
                'minute': event.timestamp.minute,
                'day_of_week': day_of_week,
                'month': month,
                'is_weekend': is_weekend,
                'lamp': event.lamp,
                'action': action
            })
        return data
    
    def train_model(self, model: NNModel, X_train: torch.Tensor, y_train: torch.Tensor, criterion, optimizer, num_epochs: int):
        for epoch in range(num_epochs):
            # Forward pass
            outputs = model(X_train)
            loss = criterion(outputs, y_train)
            
            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')
        return model
    
    def evaluate_model(self, model: NNModel, X_test_tensor: torch.Tensor, y_test_tensor: torch.Tensor):
        model.eval()
        with torch.no_grad():
            test_outputs = model(X_test_tensor)
            test_outputs = test_outputs.round()  # Convert sigmoid output to binary prediction
            accuracy = (test_outputs.eq(y_test_tensor).sum() / float(y_test_tensor.shape[0])).item()
            print(f'Accuracy on test data: {accuracy * 100:.2f}%')

    def generate_24_hour_minute_timestamps(self, date: datetime):
        timestamps = [date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(minutes=i) for i in range(1440)]
        return timestamps

    def create_24_hour_schedule(self, lamp_names, timestamps, model, feature_columns) -> Schedule:
        schedule = []
        previous_action = None  # Initialize the previous action as None

        for timestamp in timestamps:
            for lamp in lamp_names:
                # Extract features for the current timestamp and lamp
                hour = timestamp.hour
                minute = timestamp.minute
                day_of_week = timestamp.weekday()
                month = timestamp.month
                is_weekend = 1 if day_of_week >= 5 else 0

                # Create a DataFrame with the features
                feature_data = {
                    'hour': hour,
                    'minute': minute,
                    'day_of_week': day_of_week,
                    'month': month,
                    'is_weekend': is_weekend,
                    'lamp': lamp  # One-hot encoding of the lamp will be handled below
                }
                feature_df = pd.DataFrame([feature_data])

                # One-hot encode the lamp field
                feature_df = pd.get_dummies(feature_df, columns=['lamp'], prefix='lamp', dtype=float)

                # Ensure all feature columns are present
                for col in feature_columns:
                    if col not in feature_df.columns:
                        feature_df[col] = 0.0

                # Reorder columns to match the training data
                feature_df = feature_df[feature_columns]

                # Convert to tensor
                input_tensor = torch.tensor(feature_df.values, dtype=torch.float32)

                # Get the model prediction
                prediction = model(input_tensor).item()

                # Determine the action based on the prediction
                action = LampAction.ON if prediction >= 0.5 else LampAction.OFF

                # Append to schedule only if the action is different from the previous action
                if action != previous_action:
                    schedule.append(LampEvent(timestamp, lamp, action))
                    previous_action = action  # Update the previous action
        schedule.sort(key=lambda x: x.timestamp.hour * 60 + x.timestamp.minute)
        return Schedule(events=schedule)