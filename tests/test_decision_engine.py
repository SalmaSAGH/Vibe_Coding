import pytest
from services.strategies.irrigation_strategy import TomatoIrrigationStrategy

class TestIrrigationStrategy:
    def setup_method(self):
        self.strategy = TomatoIrrigationStrategy()
    
    def test_critical_moisture_triggers_immediate_watering(self):
        reading = {
            'sensor_id': 'TEST_01',
            'soil_moisture': 15.0,
            'temperature': 25.0,
            'humidity': 50.0
        }
        history = []
        result = self.strategy.calculate(reading, history)
        assert result['action'] == 'WATER_IMMEDIATELY'
        assert result['priority'] == 'critical'
        assert result['amount_L'] > 0
        assert 'Critical' in result['explanation']
    
    def test_optimal_moisture_no_action(self):
        reading = {
            'sensor_id': 'TEST_01',
            'soil_moisture': 70.0,
            'temperature': 25.0,
            'humidity': 50.0
        }
        history = []
        result = self.strategy.calculate(reading, history)
        assert result['action'] == 'MONITOR'
        assert result['amount_L'] == 0
    
    @pytest.mark.parametrize("moisture,temp,expected_action", [
        (15, 25, 'WATER_IMMEDIATELY'),
        (35, 32, 'WATER'),
        (70, 25, 'MONITOR'),
        (90, 25, 'STOP'),
    ])
    def test_various_scenarios(self, moisture, temp, expected_action):
        reading = {
            'sensor_id': 'TEST_01',
            'soil_moisture': moisture,
            'temperature': temp,
            'humidity': 50.0
        }
        result = self.strategy.calculate(reading, [])
        assert result['action'] == expected_action
