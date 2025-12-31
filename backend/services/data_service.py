# ===== services/data_service.py =====
import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict

class DataService:
    """
    Data access layer - Repository pattern
    ✅ Good: Abstracts database operations
    ⚠️ ISSUE: No transaction management for complex operations
    """
    
    def __init__(self, db: sqlite3.Connection):
        self.db = db
    
    def save_sensor_reading(self, sensor_id: str, soil_moisture: float,
                          temperature: float, humidity: float,
                          timestamp: datetime) -> dict:
        """
        Save a new sensor reading
        ✅ Good: Returns created object
        ⚠️ ISSUE: No duplicate detection
        """
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO sensor_readings 
            (sensor_id, soil_moisture, temperature, humidity, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (sensor_id, soil_moisture, temperature, humidity, timestamp))
        
        reading_id = cursor.lastrowid
        
        return {
            "id": reading_id,
            "sensor_id": sensor_id,
            "soil_moisture": soil_moisture,
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": timestamp
        }
    
    def get_latest_reading(self, sensor_id: str) -> Optional[dict]:
        """
        Get most recent reading for a sensor
        """
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT * FROM sensor_readings
            WHERE sensor_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (sensor_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_sensor_history(self, sensor_id: str, limit: int = 100) -> List[dict]:
        """
        Get historical readings
        ⚠️ ISSUE: No pagination support for large datasets
        """
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT * FROM sensor_readings
            WHERE sensor_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (sensor_id, limit))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_all_sensors(self) -> List[dict]:
        """
        Get list of all sensors with their latest reading
        ⚠️ ISSUE: Inefficient for many sensors (N+1 query problem)
        """
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT DISTINCT sensor_id FROM sensor_readings
        """)
        
        sensor_ids = [row[0] for row in cursor.fetchall()]
        
        sensors = []
        for sensor_id in sensor_ids:
            latest = self.get_latest_reading(sensor_id)
            if latest:
                sensors.append(latest)
        
        return sensors
    
    def save_recommendation(self, sensor_id: str, recommendation: dict) -> int:
        """
        Save a recommendation to database
        ✅ Good: Audit trail of recommendations
        """
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO recommendations
            (sensor_id, recommendation_data, timestamp)
            VALUES (?, ?, ?)
        """, (sensor_id, json.dumps(recommendation), datetime.utcnow()))
        
        return cursor.lastrowid
    
    def get_recommendations_history(self, sensor_id: str, limit: int = 50) -> List[dict]:
        """
        Get historical recommendations
        """
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT * FROM recommendations
            WHERE sensor_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (sensor_id, limit))
        
        rows = cursor.fetchall()
        recommendations = []
        for row in rows:
            rec = dict(row)
            rec["recommendation_data"] = json.loads(rec["recommendation_data"])
            recommendations.append(rec)
        
        return recommendations