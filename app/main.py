from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.web.app_router import app_api_router
from gcp.FirestoreService import FirestoreService
from mqtt.mqtt_client import MqttClient


firestore = FirestoreService()

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

