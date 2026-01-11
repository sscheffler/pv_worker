from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.web.app_router import app_api_router
from app.gcp.FirestoreService import FirestoreService
from app.mqtt.mqtt_client import MqttClient
from app.logging_configuration import create_logger

firestore = FirestoreService()
logger = create_logger(name=__name__)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    firestore.push_value(float(message))

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    client = MqttClient(on_message=on_message)
    client.connect()
    yield


app = FastAPI(lifespan=lifespan)

# Setting up routes for FastApi
app.include_router(router=app_api_router)

