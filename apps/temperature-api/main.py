from datetime import datetime
import random

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Temperature API")


class TemperatureResponse(BaseModel):
    sensor_id: str
    location: str
    value: float
    unit: str
    timestamp: datetime


@app.get("/temperature", response_model=TemperatureResponse)
async def get_temperature(
    location: str = Query(None, description="Room name"),
    sensor_id: str = Query(None, description="Sensor ID")
):
    if not location and sensor_id:
        location_map = {
            "1": "Living Room",
            "2": "Bedroom",
            "3": "Kitchen"
        }
        location = location_map.get(sensor_id, "Unknown")

    if not sensor_id and location:
        sensor_map = {
            "Living Room": "1",
            "Bedroom": "2",
            "Kitchen": "3"
        }
        sensor_id = sensor_map.get(location, "0")

    temperature = round(random.uniform(15.0, 35.0), 1)

    return TemperatureResponse(
        sensor_id=sensor_id,
        location=location or "Unknown",
        value=temperature,
        unit="Celsius",
        timestamp=datetime.now()
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
