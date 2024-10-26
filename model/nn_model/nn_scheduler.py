from datetime import datetime, timedelta
from typing import List
import pandas as pd
from pandas import DataFrame, Series
from sklearn.model_selection import train_test_split
import torch
from model.events.lamp_action import LampAction
from model.events.lamp_event import LampEvent
from model.nn_model.linear_model import LinearModel
from model.nn_model.time_duration_predictor import TimeDurationPredictor
from model.schedule import Schedule
from model.algorithm.abstract_mimicking_algorithm import MimickingAlgorithm

class NNScheduler(MimickingAlgorithm):
    DAY_SEGMENT_COUNT = 12
    EPOCH_COUNT = 100
    LEARNING_RATE = 0.001
    MIN_DURATION = 5
    
    def __init__(self):
        super().__init__()

    def createSchedule(self, user_actions: list[LampEvent]) -> Schedule:
        # Prepare the data
        print('Formatting data...')

        # Map lamp names to integers, used for one-hot encoding
        lamp_id_map = {lamp: i for i, lamp in enumerate(set(event.lamp for event in user_actions))}        
        
        features, target, lamp_names, duration_range = self.format_data(user_actions, lamp_id_map)
        X_train, X_test, y_train, y_test = self.split_data(features, target)
        X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor = self.to_tensors(X_train, X_test, y_train, y_test)

        # Initialize the model
        print('Init model...')
        input_size = X_train_tensor.shape[1] # The number of features
        model: TimeDurationPredictor = LinearModel(input_size)

        # Loss function and optimizer
        criterion = torch.nn.HuberLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=self.LEARNING_RATE)

        # Train the model
        print('Training model...')
        model.train(X_train_tensor, y_train_tensor, criterion, optimizer, epochs=self.EPOCH_COUNT)

        # Evaluate the model
        print('Evaluating model...')
        evaluation_metrics = model.evaluate(X_test_tensor, y_test_tensor)
        print(evaluation_metrics)

        # Generate a 24-hour schedule
        print('Generating schedule...')
        schedule = self.create_24_hour_schedule(model, lamp_names, duration_range[0], duration_range[1])

        return schedule

    def format_data(self, user_actions: list[LampEvent], lamp_id_map: dict[str, int]) -> tuple[DataFrame, DataFrame, list[str], tuple[int, int]]:
        # Generate timespans for each lamp event
        data = self.generate_timespans(user_actions)

        # Split the day into segments
        data = self.split_day_to_segments(data, self.DAY_SEGMENT_COUNT) 
        
        # Create a pandas DataFrame
        df = DataFrame(data)
        print(df)

        # Normalize the start and length columns
        min_duration = df['length'].min()
        max_duration = df['length'].max()
        duration_range = (min_duration, max_duration)
        df['start'] = df['start'].apply(lambda x: self.normalize_start_time(x))
        df['length'] = df['length'].apply(lambda x: self.normalize_duration(x, min_duration, max_duration))

        # Get the unique lamp names, used for generating the schedule
        original_lamp_names = df['lamp'].unique().tolist()
        
        # Map the lamp names to integers
        df['lamp'] = df['lamp'].map(lamp_id_map)
        print(df)

        # One-hot encode the lamp field
        df = pd.get_dummies(df, columns=['lamp', 'segment'], prefix=['lamp', 'segment'], dtype=int)
        self.add_missing_segments(df, self.DAY_SEGMENT_COUNT)

        # Reorder columns
        lamp_columns = [col for col in df.columns if col.startswith('lamp_')]
        segment_columns = sorted([col for col in df.columns if col.startswith('segment_')], key=lambda x: int(x.split('_')[-1]))
        df = df[lamp_columns + segment_columns + ['start', 'length']]

        # Split features and target
        features = df.drop(['start', 'length'], axis=1)
        target = df[['start', 'length']]

        return features, target, original_lamp_names, duration_range
    
    def split_day_to_segments(self, events: list[dict], segment_count: int) -> list[LampEvent]:
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
    
    def add_missing_segments(self, df: DataFrame, segment_count: int) -> DataFrame:
        # Add missing segments to the DataFrame
        for segment in range(segment_count):
            if f'segment_{segment}' not in df.columns:
                df[f'segment_{segment}'] = 0
        return df

    def split_data(self, features: DataFrame, target: DataFrame) -> tuple[DataFrame, DataFrame, Series, Series]:
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
    
    def create_24_hour_schedule(self, model: TimeDurationPredictor, lamp_names: list[str], min_duration: int, max_duration: int) -> Schedule:
        schedule_events = []
        lamp_id_to_int = {lamp: i for i, lamp in enumerate(lamp_names)}
        for lamp_id in lamp_id_to_int.keys():
            for segment in range(self.DAY_SEGMENT_COUNT):
                # One-hot encode the segment
                segment_one_hot = torch.zeros(self.DAY_SEGMENT_COUNT)
                segment_one_hot[segment] = 1.0

                # One-hot encode the lamp ID
                lamp_one_hot = torch.zeros(len(lamp_names))
                lamp_one_hot[lamp_id_to_int[lamp_id]] = 1.0

                # Concatenate the one-hot encoded segment and lamp ID
                sequence_tensor = torch.cat((lamp_one_hot, segment_one_hot), dim=0).unsqueeze(0)
                
                time_to_turn_on, duration = model.predict(sequence_tensor)
                turn_on_minute = round(self.denormalize_start_time(time_to_turn_on.item()))
                duration_minutes = round(self.denormalize_duration(duration.item(), min_duration, max_duration))
                
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

    def append_to_schedule(self, schedule_events: list[LampEvent], lamp: str, turn_on_minute: int, duration: int) -> None:
        if duration < self.MIN_DURATION:
            return
        
        on_timestamp = datetime.today().replace(hour=turn_on_minute // 60, minute=turn_on_minute % 60, second=0, microsecond=0)
        off_timestamp = on_timestamp + timedelta(minutes=duration)
        
        # Check if the lamp is already scheduled to be on
        prev_event = None
        for event in schedule_events[::-1]:
            if event.lamp == lamp and event.timestamp <= on_timestamp:
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
                if event.lamp == lamp and event.action == LampAction.OFF and event.timestamp > on_timestamp:
                    prev_off_event = event
                    break

            # Update off event timestamp to the new off timestamp
            if prev_off_event:
                prev_off_event.timestamp = off_timestamp
            else:
                # Append OFF event if no previous OFF event is found
                schedule_events.append(LampEvent(lamp=lamp, timestamp=off_timestamp, action=LampAction.OFF))

    # Denormalizing start time
    # Normalizing start time (minute of the day)
    def normalize_start_time(self, start_time):
        return start_time / 1440  # Normalizing to the range [0, 1]

    # Normalizing duration with a given range [min_duration, max_duration]
    def normalize_duration(self, duration, min_duration=1, max_duration=120):
        return (duration - min_duration) / (max_duration - min_duration)
    
    # Denormalizing start time
    def denormalize_start_time(self, normalized_start_time):
        return normalized_start_time * 1440

    # Denormalizing duration
    def denormalize_duration(self, normalized_duration, min_duration=1, max_duration=120):
        return normalized_duration * (max_duration - min_duration) + min_duration