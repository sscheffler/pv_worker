from paho.mqtt import client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion

from app.app_configuration import get_settings, MqttSettings
from app.logging_configuration import create_logger

logger = create_logger(name=__name__)

class MqttClient:
    def __init__(self, on_message):
        self.settings: MqttSettings = get_settings().MQTT
        self.client = mqtt_client.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=self.settings.client_id,
        )
        self.client.on_connect = self.on_connect
        self.client.on_message = on_message

    def connect(self):
        logger.info("Connecting to MQTT Broker")
        self.client.connect(self.settings.broker, self.settings.port)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            logger.info(f"Connected to MQTT Broker {rc}!")
        else:
            logger.error(f"Failed to connect, return code {rc}\n", rc)
        self.client.subscribe(self.settings.topic)
