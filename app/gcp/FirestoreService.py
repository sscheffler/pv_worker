from datetime import datetime, timezone
from google.cloud import firestore

from app_configuration import get_settings
from logging_configuration import create_logger

logger = create_logger(name=__name__)


class FirestoreService:

    def __init__(self):
        self.settings = get_settings().FIRESTORE
        self.db = firestore.Client()

    def push_value(self, value: float):
        now = datetime.now(tz=timezone.utc)
        logger.info(f"Pushing value {value} to Firestore(collection={self.settings.collection}) at {now}")
        if value > 0:
            self.db.collection(self.settings.collection).add({
                "value": value,
                "time": now,
            })
        else:
            logger.info(f"Value {value} is 0 or negative, not pushing to Firestore")
