from datetime import datetime, timezone, timedelta
from google.cloud import firestore

from app.app_configuration import get_settings
from app.logging_configuration import create_logger

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
            logger.info(f"Pushing value {value} to Firestore(collection={self.settings.collection}) at {now}")
            if value > 0:
                self.db.collection(self.settings.collection).add({
                    "value": value,
                    "time": now,
                })
            else:
                logger.info(f"Value {value} is 0 or negative, not pushing to Firestore")
            self.last_push_time = now
