# ===== models.py =====
from datetime import datetime
from typing import Optional

class SensorReading:
    """Sensor reading model"""
    def __init__(self, id: Optional[int], sensor_id: str, soil_moisture: float,
                 temperature: float, humidity: float, timestamp: datetime):
        self.id = id
        self.sensor_id = sensor_id
        self.soil_moisture = soil_moisture
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp
    
    def to_dict(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "soil_moisture": self.soil_moisture,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp
        }

class Recommendation:
    """Recommendation model"""
    def __init__(self, sensor_id: str, irrigation: dict, 
                 fertilization: dict, alerts: list, timestamp: datetime):
        self.sensor_id = sensor_id
        self.irrigation = irrigation
        self.fertilization = fertilization
        self.alerts = alerts
        self.timestamp = timestamp
    
    def to_dict(self):
        return {
            "sensor_id": self.sensor_id,
            "timestamp": self.timestamp.isoformat(),
            "irrigation": self.irrigation,
            "fertilization": self.fertilization,
            "alerts": self.alerts
        }