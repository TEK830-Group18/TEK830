import torch
from torch.utils.data import Dataset
from model.events.lamp_event import LampEvent
from model.events.lamp_action import LampAction

class LampEventDataset(Dataset):
    def __init__(self, lamp_events: list[LampEvent], sequence_length: int=10):
        self.lamp_events: list[LampEvent] = lamp_events
        self.sequence_length: int = sequence_length
        self.lamp_id_to_int = self.create_lamp_id_mapping()
        self.data = self.prepare_data()

    def create_lamp_id_mapping(self):
        # Create a mapping from lamp_id to a unique integer
        unique_lamp_ids = set(event.lamp for event in self.lamp_events)
        return {lamp_id: i for i, lamp_id in enumerate(unique_lamp_ids)}

    def prepare_data(self):
        # Convert lamp events to time-series sequences with time difference and action
        sequences = []
        for i in range(len(self.lamp_events) - self.sequence_length):
            seq = self.lamp_events[i:i+self.sequence_length]
            next_event = self.lamp_events[i + self.sequence_length]
            time_diff = (next_event.timestamp - seq[-1].timestamp).total_seconds()  # Time difference in seconds
            target_action = next_event.action  # Next action (on/off)
            sequences.append((seq, time_diff, target_action))
        return sequences

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sequence, time_diff, target_action = self.data[idx]
        
        # Extract features from the sequence
        timestamps = [event.timestamp.timestamp() for event in sequence]  # Convert datetime to timestamp
        lamp_ids = [self.lamp_id_to_int[event.lamp] for event in sequence]  # Convert lamp_id to integer
        actions = [1.0 if event.action == LampAction.ON else 0.0 for event in sequence]  # Convert actions to binary
        
        # Convert to tensors
        timestamps_tensor = torch.tensor(timestamps, dtype=torch.float32).unsqueeze(1)  # Shape (sequence_length, 1)
        lamp_ids_tensor = torch.tensor(lamp_ids, dtype=torch.float32).unsqueeze(1)  # Shape (sequence_length, 1)
        actions_tensor = torch.tensor(actions, dtype=torch.float32).unsqueeze(1)  # Shape (sequence_length, 1)
        time_diff_tensor = torch.tensor([time_diff], dtype=torch.float32)  # Shape (1,)
        target_action_tensor = torch.tensor([1.0 if target_action == LampAction.ON else 0.0], dtype=torch.float32)  # Shape (1,)
        
        # Concatenate features along the feature dimension
        sequence_tensor = torch.cat((timestamps_tensor, lamp_ids_tensor, actions_tensor), dim=1)  # Shape (sequence_length, 3)
        
        return sequence_tensor, time_diff_tensor, target_action_tensor