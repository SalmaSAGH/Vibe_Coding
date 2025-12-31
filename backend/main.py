from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
import uvicorn

from database import get_db, init_db
from models import SensorReading, Recommendation
from services.decision_engine import DecisionEngine
from services.data_service import DataService

app = FastAPI(
    title="Smart Agriculture API",
    description="Decision Support System for Smart Agriculture",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ SECURITY ISSUE: Should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# ===== Request/Response Models =====
class SensorDataRequest(BaseModel):
    sensor_id: str = Field(..., min_length=1, max_length=50)
    soil_moisture: float = Field(..., ge=0, le=100)
    temperature: float = Field(..., ge=-50, le=60)
    humidity: float = Field(..., ge=0, le=100)
    timestamp: Optional[datetime] = None
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        return v or datetime.utcnow()

class SensorDataResponse(BaseModel):
    id: int
    sensor_id: str
    soil_moisture: float
    temperature: float
    humidity: float
    timestamp: datetime
    
class RecommendationResponse(BaseModel):
    sensor_id: str
    timestamp: datetime
    irrigation: dict
    fertilization: dict
    alerts: List[str]

# ===== Endpoints =====
@app.post("/api/sensors/data", response_model=SensorDataResponse, status_code=201)
async def ingest_sensor_data(data: SensorDataRequest, db=Depends(get_db)):
    """
    Ingest new sensor data
    ⚠️ ISSUE: No authentication
    ⚠️ ISSUE: No rate limiting
    """
    try:
        data_service = DataService(db)
        reading = data_service.save_sensor_reading(
            sensor_id=data.sensor_id,
            soil_moisture=data.soil_moisture,
            temperature=data.temperature,
            humidity=data.humidity,
            timestamp=data.timestamp
        )
        return reading
    except Exception as e:
        # ⚠️ ISSUE: Exposing internal errors to client
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sensors/current/{sensor_id}")
async def get_current_data(sensor_id: str, db=Depends(get_db)):
    """
    Get latest reading for a sensor
    """
    data_service = DataService(db)
    reading = data_service.get_latest_reading(sensor_id)
    
    if not reading:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return reading

@app.get("/api/sensors/history/{sensor_id}")
async def get_sensor_history(
    sensor_id: str, 
    limit: int = 100,  # ⚠️ ISSUE: No max limit enforcement
    db=Depends(get_db)
):
    """
    Get historical data for a sensor
    """
    data_service = DataService(db)
    history = data_service.get_sensor_history(sensor_id, limit)
    return {"sensor_id": sensor_id, "readings": history}

@app.get("/api/recommendations/{sensor_id}", response_model=RecommendationResponse)
async def get_recommendations(sensor_id: str, db=Depends(get_db)):
    """
    Generate recommendations for a sensor
    ✅ Good: Clear purpose
    ⚠️ ISSUE: No caching, recalculates every time
    """
    data_service = DataService(db)
    reading = data_service.get_latest_reading(sensor_id)
    
    if not reading:
        raise HTTPException(status_code=404, detail="No data for sensor")
    
    # Get historical context
    history = data_service.get_sensor_history(sensor_id, limit=10)
    
    # Generate recommendation
    engine = DecisionEngine()
    recommendation = engine.generate_recommendation(reading, history)
    
    # Save recommendation
    data_service.save_recommendation(sensor_id, recommendation)
    
    return recommendation

@app.get("/api/sensors/list")
async def list_sensors(db=Depends(get_db)):
    """
    List all sensors with latest data
    """
    data_service = DataService(db)
    sensors = data_service.get_all_sensors()
    return {"sensors": sensors}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

