# ===== database.py =====
import sqlite3
from contextlib import contextmanager
from typing import Generator

DATABASE_URL = "data/agri.db"

def init_db():
    """Initialize database schema"""
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Sensor readings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            soil_moisture REAL NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            timestamp DATETIME NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Index for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sensor_timestamp 
        ON sensor_readings(sensor_id, timestamp DESC)
    """)
    
    # Recommendations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            recommendation_data TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Database connection context manager
    ⚠️ ISSUE: No connection pooling
    ⚠️ ISSUE: Row factory not set for easy dict access
    """
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row  # ✅ Returns dict-like rows
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()