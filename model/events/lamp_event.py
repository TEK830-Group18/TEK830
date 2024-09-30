from dataclasses import dataclass, field
from typing import List, Optional
import marshmallow_dataclass
import marshmallow.validate
from datetime import datetime
from lamp_action import LampAction

@dataclass
class LampEvent:
    timestamp: datetime
    lamp: str
    action: LampAction
    
    def from_json(self, json: dict):
        return marshmallow_dataclass.class_schema(LampEvent)().load(data=json, unknown=marshmallow.EXCLUDE)
