import logging
import os

# -------------------------
# Configure Third party loggers
# -------------------------
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)
logging.getLogger("tzlocal").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# -------------------------
# Settings
# -------------------------
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s - %(message)s"
LOG_DATE_FORMAT = "%d/%m/%Y %H:%M:%S"


def setup_logging() -> None:
    """Configure root logger once."""
    root = logging.getLogger()
    root.setLevel(LOG_LEVEL)

    # Remove existing handlers to avoid duplicate logs
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler()
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
    root.addHandler(handler)


def create_logger(name: str = "APP"):
    return logging.getLogger(name=name)


# -------------------------
# Initialization
# -------------------------
setup_logging()
app_logger = create_logger()
