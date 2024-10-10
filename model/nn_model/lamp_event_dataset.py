import torch
from torch.utils.data import Dataset
from model.events.lamp_event import LampEvent
from model.events.lamp_action import LampAction
from datetime import datetime, timedelta

class LampEventDataset(Dataset):
    def __init__(self, lamp_events: list[LampEvent]):
        self.lamp_events: list[LampEvent] = lamp_events
        self.lamp_id_to_int = self.create_lamp_id_mapping()
        self.data = self.prepare_data()

    def create_lamp_id_mapping(self):
        # Create a mapping from lamp_id to a unique integer
        unique_lamp_ids = set(event.lamp for event in self.lamp_events)
        return {lamp_id: idx for idx, lamp_id in enumerate(unique_lamp_ids)}

    def prepare_data(self):
        actions_map: dict[str, list[LampEvent]] = self.map_actions_to_id()

        # Prepare data for every minute in a day
        sequences = []
        for lamp_id in self.lamp_id_to_int.keys():
            for minute in range(1440):  # 1440 minutes in a day
                time_of_day = minute
                state = self.get_state_for_minute(lamp_id, minute, actions_map[lamp_id])
                sequences.append((time_of_day, self.lamp_id_to_int[lamp_id], state))
        return sequences

    def map_actions_to_id(self) -> dict[str, list[LampEvent]]:
        # Map lamp events to a dictionary of lamp_id to list of events
        map: dict[str, list[LampEvent]] = {}
        for event in self.lamp_events:
            map.setdefault(event.lamp, []).append(event)
        
        # Sort the events by timestamp
        for lamp_id in map.keys():
            map[lamp_id].sort(key=lambda x: x.timestamp)

        return map

    def get_state_for_minute(self, lamp_id: str, minute: int, events: list[LampEvent]) -> int:
        if len(events) == 0:
            raise ValueError("No events found for lamp_id: {}".format(lamp_id))

        # Get the state of the lamp for a given minute
        hi, lo = 0, len(events) - 1
        event_time = events[lo].timestamp.hour * 60 + events[lo].timestamp.minute
        mid = (hi + lo) // 2
        while hi < lo:
            mid = (hi + lo) // 2
            event_time = events[mid].timestamp.hour * 60 + events[mid].timestamp.minute
            if event_time == minute:
                break
            elif event_time < minute:
                hi = mid + 1
            else:
                lo = mid

        return 1 if events[mid].action == LampAction.ON else 0

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        time_of_day, lamp_id, action = self.data[idx]
        
        # Convert to tensors
        time_of_day_tensor = torch.tensor([time_of_day], dtype=torch.float32)
        lamp_id_tensor = torch.tensor([lamp_id], dtype=torch.float32)
        action_tensor = torch.tensor([action], dtype=torch.float32)
        
        # Concatenate features along the feature dimension
        sequence_tensor = torch.cat((time_of_day_tensor, lamp_id_tensor), dim=0)  # Shape (2,)
        
        return sequence_tensor, action_tensor
    