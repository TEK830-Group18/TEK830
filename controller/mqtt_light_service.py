from abstract_light_service import AbstractLightService
from model.events.lamp_event import LampEvent
import json
import paho.mqtt.client as mqtt

class MqttLightService(AbstractLightService):
    """
    A service class that handles events related to MQTT-controlled lights.
    Attributes:
        mqtt_address (str): The address of the MQTT broker.
        mqtt_port (int): The port of the MQTT broker. Defaults to 1883.
        base_topic (str): The base topic for MQTT messages.
    Methods:
        handle_event(event: LampEvent) -> None:
            Handles a LampEvent by publishing the event to the appropriate MQTT topic.
    """

    mqtt_address: str
    mqtt_port: int = 1883
    base_topic: str
    client: mqtt.Client

    def __init__(self, mqtt_client: str, mqtt_port: int, topic: str) -> None:
        self.mqtt_address = mqtt_client
        self.mqtt_port = mqtt_port
        self.base_topic = topic
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def handle_event(self, event: LampEvent) -> None:
        """
        Handles the given LampEvent by publishing it to the MQTT broker. Message is formatted for zigbee2mqtt.
        """

        topic = f"{self.base_topic}/{event.lamp}"
        payload = self.__translate_event(event)

        try:
            self.client.connect(self.mqtt_address, self.mqtt_port)
            self.client.publish(topic, payload)
            self.client.disconnect()
        except Exception as e:
            print(f"Error: {e}")

    def __translate_event(self, event: LampEvent) -> str:
        return json.dumps({f'state': event.action.value})
    