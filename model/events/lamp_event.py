from dataclasses import dataclass, field
from typing import Optional
from marshmallow import Schema, fields, post_load
import marshmallow_dataclass
import marshmallow
from datetime import datetime
import time
from model.events.lamp_action import LampAction
from model.events.abstract_event import Event


class LampEventSchema(Schema):
    timestamp = fields.DateTime()
    lamp = fields.String()
    action = fields.String()

    @post_load
    def make_lamp_event(self, data, **kwargs) -> 'LampEvent':
        data['action'] = LampAction(data['action'])
        return LampEvent(**data)

@dataclass(order=True)
class LampEvent(Event):
    sort_index: int = field(init=False, repr=False)
    timestamp: datetime
    lamp: str
    action: LampAction

    def __post_init__(self):
        unixTime = time.mktime(self.timestamp.timetuple())
        self.sort_index = int(unixTime)

    @staticmethod
    def from_json(json_data: dict) -> 'LampEvent':
        schema = LampEventSchema()
        loaded = schema.load(json_data, unknown=marshmallow.EXCLUDE)
        return loaded # type: ignore