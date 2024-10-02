from dataclasses import dataclass
from typing import Optional
from marshmallow import Schema, fields, post_load
import marshmallow_dataclass
import marshmallow
from datetime import datetime
from model.events.lamp_action import LampAction


class LampEventSchema(Schema):
    timestamp: fields.DateTime
    lamp: fields.String
    action: fields.String

    @post_load
    def make_lamp_event(self, data, **kwargs) -> 'LampEvent':
        return LampEvent(**data)

@dataclass
class LampEvent:
    timestamp: datetime
    lamp: str
    action: LampAction

    @staticmethod
    def from_json(json_data: dict) -> 'LampEvent':
        schema = LampEventSchema()
        loaded = schema.load(json_data, unknown=marshmallow.EXCLUDE)
        lamp_event = schema.make_lamp_event(loaded)
        return lamp_event