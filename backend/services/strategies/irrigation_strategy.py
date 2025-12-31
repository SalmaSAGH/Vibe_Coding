from abc import ABC, abstractmethod
from typing import Dict, List
from config.settings import get_settings
from datetime import datetime

class IrrigationStrategy(ABC):
    """Abstract base class for irrigation strategies"""
    
    @abstractmethod
    def calculate(self, reading: dict, history: List[dict]) -> dict:
        """Calculate irrigation recommendation"""
        pass

class TomatoIrrigationStrategy(IrrigationStrategy):
    """Irrigation strategy specific to tomato crops"""
    
    def __init__(self):
        self.settings = get_settings()
    
    def calculate(self, reading: dict, history: List[dict]) -> dict:
        moisture = reading['soil_moisture']
        temp = reading['temperature']
        
        if moisture < self.settings.soil_moisture_critical:
            return self._critical_response(moisture, temp)
        if moisture < self.settings.soil_moisture_low:
            return self._low_moisture_response(moisture, temp, history)
        if moisture > self.settings.soil_moisture_excess:
            return self._excess_moisture_response(moisture)
        return self._optimal_response(moisture)
    
    def _critical_response(self, moisture: float, temp: float) -> dict:
        return {
            'action': 'WATER_IMMEDIATELY',
            'amount_L': self._calculate_amount(
                self.settings.soil_moisture_optimal_min, 
                moisture, 
                temp
            ),
            'priority': 'critical',
            'explanation': f"Critical: Soil moisture {moisture:.1f}% below wilting point. Immediate action required.",
            'timing': 'NOW',
            'next_check_hours': 4
        }
    
    def _calculate_amount(self, target: float, current: float, temp: float) -> float:
        deficit = (target - current) / 100
        base_amount = self.settings.default_plot_area_m2 * self.settings.root_depth_m * deficit * 1000
        temp_factor = 1.0 + max(0, (temp - 25) * 0.02)
        return round(base_amount * temp_factor, 1)

class LettuceIrrigationStrategy(IrrigationStrategy):
    """Different thresholds for lettuce"""
    
    def __init__(self):
        self.settings = get_settings()
        self.moisture_low = 50.0
        self.moisture_optimal_min = 70.0
    
    def calculate(self, reading: dict, history: List[dict]) -> dict:
        pass  # Lettuce-specific logic
