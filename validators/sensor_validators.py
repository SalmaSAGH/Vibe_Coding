from pydantic import validator, Field, BaseModel
from datetime import datetime, timedelta
from typing import Optional

class SensorDataRequest(BaseModel):
    sensor_id: str = Field(..., min_length=1, max_length=50, regex="^[a-zA-Z0-9_-]+$")
    soil_moisture: float = Field(..., ge=0, le=100)
    temperature: float = Field(..., ge=-50, le=60)
    humidity: float = Field(..., ge=0, le=100)
    timestamp: Optional[datetime] = None
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        """Ensure timestamp is recent and not in future"""
        if v is None:
            return datetime.utcnow()
        
        if isinstance(v, datetime):
            now = datetime.utcnow()
            if v > now + timedelta(minutes=5):
                raise ValueError("Timestamp cannot be in future")
            if v < now - timedelta(days=7):
                raise ValueError("Timestamp too old (>7 days)")
        return v
    
    @validator('sensor_id')
    def validate_sensor_id(cls, v):
        """Prevent SQL injection via sensor_id"""
        if any(char in v for char in ["'", '"', ";", "--", "/*"]):
            raise ValueError("Invalid characters in sensor_id")
        return v
