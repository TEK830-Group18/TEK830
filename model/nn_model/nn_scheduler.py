from datetime import datetime, timedelta
import math
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
from progressbar import progressbar


class NNScheduler(Scheduler):
    DAY_SEGMENT_COUNT = 12
    EPOCH_COUNT = 40
    
    def __init__(self):
        super().__init__()

    def createSchedule(self, user_actions: List[LampEvent]) -> Schedule:
        # Prepare the data
        print('Formatting data...')

        # Map lamp names to integers, used for one-hot encoding
        lamp_id_map = {lamp: i for i, lamp in enumerate(set(event.lamp for event in user_actions))}        
        
        features, target, lamp_names = self.format_data(user_actions, lamp_id_map)
        X_train, X_test, y_train, y_test = self.split_data(features, target)
        X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor = self.to_tensors(X_train, X_test, y_train, y_test)

        # Initialize the model
        print('Init model...')
        input_size = X_train_tensor.shape[1] # The number of features
        model: NNModel = NNModel(input_size)

        # Loss function and optimizer
        criterion = torch.nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

        # Train the model
        print('Training model...')
        self.train_model(model, X_train_tensor, y_train_tensor, criterion, optimizer, num_epochs=self.EPOCH_COUNT)

        # Evaluate the model
        # print('Evaluating model...')
        # self.evaluate_model(model, X_test_tensor, y_test_tensor)

        # Generate a 24-hour schedule
        print('Generating schedule...')
        schedule = self.create_24_hour_schedule(model, lamp_names)

        return schedule

    def format_data(self, user_actions: List[LampEvent], lamp_id_map: dict[str, int]) -> tuple[DataFrame, DataFrame, list[str]]:
        # Generate timespans for each lamp event
        data = self.generate_timespans(user_actions)

        # Split the day into segments
        data = self.split_day_to_segments(data, self.DAY_SEGMENT_COUNT) 
        
        # Create a pandas DataFrame
        df = DataFrame(data)
        print(df)

        # Get the unique lamp names, used for generating the schedule
        original_lamp_names = df['lamp'].unique().tolist()
        
        # Map the lamp names to integers
        df['lamp'] = df['lamp'].map(lamp_id_map)
        print(df)

        # One-hot encode the lamp field
        df = pd.get_dummies(df, columns=['lamp'], prefix='lamp', dtype=int)

        # Split features and target
        features = df.drop(['start', 'length'], axis=1)
        target = df[['start', 'length']]

        return features, target, original_lamp_names
    
    def split_day_to_segments(self, events: list[LampEvent], segment_count: int) -> list[LampEvent]:
        split_events = []
        segment_threshold = 1440 / segment_count
        for event in events:
            segment = int((event['start'].hour * 60 + event['start'].minute) // segment_threshold)
            split_events.append({
                'lamp': event['lamp'],
                'start': event['start'].hour * 60 + event['start'].minute,
                'length': event['length'],
                'segment': segment,
            })
        return split_events
    
    def split_data(self, features: DataFrame, target: Series) -> tuple[DataFrame, DataFrame, Series, Series]:
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    
    def to_tensors(self, X_train, X_test, y_train, y_test) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
        y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).unsqueeze(1)  # Convert to (N, 1) shape
        X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
        y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).unsqueeze(1)  # Convert to (N, 1) shape
        return X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor
    
    def generate_timespans(self, events: list[LampEvent]) -> list[dict]:
        # Generate timespans for each lamp event with a start time and duration
        timespans = []
        events.sort(key=lambda x: x.timestamp)
        for i, event in enumerate(events):
            if event.action == LampAction.ON:
                lamp = event.lamp
                start = event.timestamp
                end = None
                for j in range(i + 1, len(events)):
                    if events[j].action == LampAction.OFF:
                        end = events[j].timestamp
                        break
                if end is not None:
                    timespans.append({'lamp': lamp, 'start': start, 'length': (end - start).total_seconds() // 60})
        return timespans
    
    def train_model(self, model: NNModel, X_train: torch.Tensor, y_train: torch.Tensor, criterion, optimizer, num_epochs: int):
        for epoch in range(num_epochs):
            # Forward pass
            time_to_turn_on, duration = model(X_train.float())
            
            # Squeeze the extra dimension out of y_train
            y_train = y_train.squeeze(1)
            
            # Ensure the target tensors are 1D
            time_targets = y_train[:, 0].float()
            duration_targets = y_train[:, 1].float()
            
            # Compute loss for each output
            loss_time = criterion(time_to_turn_on, time_targets)
            loss_duration = criterion(duration, duration_targets)
            
            # Combine losses
            loss = loss_time + loss_duration
            
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
            # print(f'Accuracy on test data: {accuracy * 100:.2f}%')

    def create_24_hour_schedule(self, model: NNModel, lamp_names: list[str]) -> Schedule:
        model.eval()
        schedule_events = []
        
        # lamp_id_to_int = {lamp: idx for idx, lamp in enumerate(df['lamp'].unique())}
        lamp_id_to_int = {lamp: i for i, lamp in enumerate(lamp_names)}
        
        with torch.no_grad():
            for lamp_id in lamp_id_to_int.keys():
                for segment in range(self.DAY_SEGMENT_COUNT):
                    time_of_day_tensor = torch.tensor([segment], dtype=torch.float32)
                    lamp_id_tensor = torch.tensor([lamp_id_to_int[lamp_id]], dtype=torch.float32)

                    # One-hot encode the lamp ID
                    lamp_one_hot = torch.zeros(len(lamp_names))
                    lamp_one_hot[lamp_id_to_int[lamp_id]] = 1.0


                    # Concatenate the time of day and one-hot encoded lamp ID
                    sequence_tensor = torch.cat((time_of_day_tensor, lamp_one_hot), dim=0).unsqueeze(0)
                    
                    time_to_turn_on, duration = model(sequence_tensor)
                    turn_on_minute = round(time_to_turn_on.item())
                    duration_minutes = round(duration.item())
                    
                    self.append_to_schedule(
                        schedule_events=schedule_events,
                        lamp=lamp_id,
                        turn_on_minute=turn_on_minute,
                        duration=duration_minutes
                    )
        
        schedule_events.sort(key=lambda x: x.timestamp)
        for event in schedule_events:
            print(event)
        return Schedule(events=schedule_events)
    
    def append_to_schedule(self, schedule_events: list[LampEvent], lamp: str, turn_on_minute: int, duration) -> None:
        if duration == 0:
            return
        
        on_timestamp = datetime.today().replace(hour=turn_on_minute // 60, minute=turn_on_minute % 60, second=0, microsecond=0)
        off_timestamp = on_timestamp + timedelta(minutes=duration)
        
        # Check if the lamp is already scheduled to be on
        prev_event = None
        for event in schedule_events[::-1]:
            if event.lamp == lamp and event.timestamp < on_timestamp:
                prev_event = event
                break
            if event.lamp == lamp and event.timestamp < on_timestamp:
                prev_event = event
                break
        
        if prev_event is None or prev_event.action == LampAction.OFF:
            # Append ON and OFF events to the schedule
            schedule_events.append(LampEvent(lamp=lamp, timestamp=on_timestamp, action=LampAction.ON))
            schedule_events.append(LampEvent(lamp=lamp, timestamp=off_timestamp, action=LampAction.OFF))

        else:
            # Find the previous OFF event for the lamp
            prev_off_event = None
            for event in schedule_events[::-1]:
                if event.lamp == lamp and event.timestamp < on_timestamp:
                    prev_off_event = event
                    break

            # Update off event timestamp to the new on timestamp
            if prev_off_event is None:
                return
            prev_off_event.timestamp = off_timestamp