from datetime import datetime, timezone

from logging_configuration import create_logger

logger = create_logger(name=__name__)

class FirestoreService:

    def __init__(self):
        pass

    @staticmethod
    def push_value(value: float):
        now = datetime.now(tz=timezone.utc)
        logger.info(f"Pushing value {value} to Firestore at {now}")