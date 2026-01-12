from datetime import datetime, timezone, timedelta
from google.cloud import firestore

from app.app_configuration import get_settings
from app.logging_configuration import create_logger
import random

logger = create_logger(name=__name__)


class FirestoreService:

    def __init__(self):
        self.settings = get_settings().FIRESTORE
        self.db = firestore.Client()
        self.last_push_time = datetime.now(tz=timezone.utc)

    def push_value(self, value: float):
        now = datetime.now(tz=timezone.utc)
        # Only push every 5 seconds
        if now >= self.last_push_time + timedelta(seconds=5):

            if value > 0:
                value_to_send = value
            else:
                value_to_send = round(random.uniform(1, 11), 2)
                logger.info(f"Value {value} is 0 or negative, sending random data: {value_to_send}")
            logger.info(f"Pushing value {value_to_send} to Firestore(collection={self.settings.collection}) at {now}")
            self.db.collection(self.settings.collection).add({
                "value": value_to_send,
                "time": now,
            })
            self.last_push_time = now
