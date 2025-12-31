from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestSensorEndpoints:
    def test_ingest_sensor_data_success(self):
        response = client.post(
            "/api/sensors/data",
            json={
                "sensor_id": "TEST_SENSOR",
                "soil_moisture": 50.0,
                "temperature": 25.0,
                "humidity": 60.0
            },
            headers={"X-API-Key": "test-key-123"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data['sensor_id'] == "TEST_SENSOR"
        assert data['soil_moisture'] == 50.0
    
    def test_ingest_without_api_key_fails(self):
        response = client.post(
            "/api/sensors/data",
            json={"sensor_id": "TEST", "soil_moisture": 50.0}
        )
        assert response.status_code == 401
    
    def test_invalid_moisture_value_fails(self):
        response = client.post(
            "/api/sensors/data",
            json={
                "sensor_id": "TEST",
                "soil_moisture": 150.0,
                "temperature": 25.0,
                "humidity": 60.0
            },
            headers={"X-API-Key": "test-key-123"}
        )
        assert response.status_code == 422
