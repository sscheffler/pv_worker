from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.web.app_router import app_api_router
from mqtt.mqtt_client import MqttClient


def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic} | Wert: {msg.payload.decode()} W")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    client = MqttClient(on_message=on_message)
    client.connect()
    yield


app = FastAPI(lifespan=lifespan)

# Setting up routes for FastApi
app.include_router(router=app_api_router)

