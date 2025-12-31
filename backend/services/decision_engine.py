# ===== services/decision_engine.py =====
from datetime import datetime
from typing import List, Dict
import statistics

class DecisionEngine:
    """
    Main decision engine for generating agricultural recommendations
    ⚠️ ARCHITECTURAL ISSUE: Monolithic class doing too much
    ✅ Good: Rule-based and explainable
    """
    
    def __init__(self):
        # ⚠️ ISSUE: Hardcoded thresholds should be in configuration
        self.SOIL_MOISTURE_LOW = 30
        self.SOIL_MOISTURE_HIGH = 70
        self.SOIL_MOISTURE_CRITICAL = 20
        self.TEMP_OPTIMAL_MIN = 15
        self.TEMP_OPTIMAL_MAX = 30
        self.HUMIDITY_LOW = 40
    
    def generate_recommendation(self, current_reading: dict, 
                               history: List[dict]) -> dict:
        """
        Generate complete recommendation based on current and historical data
        """
        irrigation = self._calculate_irrigation(current_reading, history)
        fertilization = self._calculate_fertilization(current_reading, history)
        alerts = self._generate_alerts(current_reading, history)
        
        return {
            "sensor_id": current_reading["sensor_id"],
            "timestamp": datetime.utcnow(),
            "irrigation": irrigation,
            "fertilization": fertilization,
            "alerts": alerts
        }
    
    def _calculate_irrigation(self, reading: dict, history: List[dict]) -> dict:
        """
        Calculate irrigation needs
        ✅ Good: Returns action + explanation
        ⚠️ ISSUE: Doesn't consider weather forecast
        """
        moisture = reading["soil_moisture"]
        temp = reading["temperature"]
        
        # Calculate trend if history available
        trend = self._calculate_moisture_trend(history)
        
        if moisture < self.SOIL_MOISTURE_CRITICAL:
            return {
                "action": "water_immediately",
                "amount_ml": 5000,
                "priority": "high",
                "explanation": f"Critical: Soil moisture at {moisture:.1f}% is below {self.SOIL_MOISTURE_CRITICAL}%. Immediate watering required to prevent crop stress."
            }
        elif moisture < self.SOIL_MOISTURE_LOW:
            # Adjust amount based on temperature
            base_amount = 3000
            temp_factor = 1.0 + (max(0, temp - 25) * 0.05)  # Increase for hot weather
            amount = int(base_amount * temp_factor)
            
            return {
                "action": "water",
                "amount_ml": amount,
                "priority": "medium",
                "explanation": f"Soil moisture at {moisture:.1f}% is below optimal range ({self.SOIL_MOISTURE_LOW}-{self.SOIL_MOISTURE_HIGH}%). Temperature is {temp:.1f}°C. {trend}"
            }
        elif moisture > self.SOIL_MOISTURE_HIGH:
            return {
                "action": "stop_watering",
                "amount_ml": 0,
                "priority": "low",
                "explanation": f"Soil moisture at {moisture:.1f}% is above optimal range. Risk of overwatering. Allow soil to dry naturally."
            }
        else:
            return {
                "action": "monitor",
                "amount_ml": 0,
                "priority": "low",
                "explanation": f"Soil moisture at {moisture:.1f}% is optimal. Continue monitoring. {trend}"
            }
    
    def _calculate_fertilization(self, reading: dict, history: List[dict]) -> dict:
        """
        Calculate fertilization needs
        ⚠️ ISSUE: Very simplistic logic, doesn't consider:
        - Crop type
        - Growth stage
        - Soil nutrients (N, P, K)
        - Last fertilization date
        """
        # Simplified heuristic: recommend fertilization every 14 days
        # In real system, this would be much more sophisticated
        
        days_since_reading = len(history)  # Rough proxy
        
        if days_since_reading > 14:
            return {
                "needed": True,
                "type": "balanced_NPK",
                "amount_kg": 2.5,
                "explanation": "Based on time elapsed, balanced fertilization recommended. Actual needs depend on soil analysis and crop type."
            }
        else:
            return {
                "needed": False,
                "type": None,
                "amount_kg": 0,
                "explanation": "No fertilization needed at this time. Monitor plant health and soil conditions."
            }
    
    def _generate_alerts(self, reading: dict, history: List[dict]) -> List[str]:
        """
        Generate alerts based on thresholds
        ✅ Good: Clear alert messages
        """
        alerts = []
        
        moisture = reading["soil_moisture"]
        temp = reading["temperature"]
        humidity = reading["humidity"]
        
        # Drought risk
        if moisture < self.SOIL_MOISTURE_CRITICAL and temp > 30:
            alerts.append(f"⚠️ DROUGHT RISK: Critical soil moisture ({moisture:.1f}%) combined with high temperature ({temp:.1f}°C)")
        
        # Overwatering risk
        if moisture > self.SOIL_MOISTURE_HIGH and humidity > 80:
            alerts.append(f"⚠️ OVERWATERING RISK: High soil moisture ({moisture:.1f}%) and humidity ({humidity:.1f}%) may cause root rot")
        
        # Temperature stress
        if temp > 35:
            alerts.append(f"🌡️ HEAT STRESS: Temperature {temp:.1f}°C exceeds optimal range. Consider shade or increased irrigation.")
        elif temp < 10:
            alerts.append(f"❄️ COLD STRESS: Temperature {temp:.1f}°C below optimal. Risk of frost damage.")
        
        # Low humidity alert
        if humidity < self.HUMIDITY_LOW:
            alerts.append(f"💨 LOW HUMIDITY: {humidity:.1f}% humidity may increase water stress. Monitor closely.")
        
        return alerts
    
    def _calculate_moisture_trend(self, history: List[dict]) -> str:
        """
        Calculate moisture trend from historical data
        ⚠️ ISSUE: Simplistic calculation, could use linear regression
        """
        if len(history) < 3:
            return ""
        
        recent = [h["soil_moisture"] for h in history[:3]]
        avg_recent = statistics.mean(recent)
        
        if len(history) >= 6:
            older = [h["soil_moisture"] for h in history[3:6]]
            avg_older = statistics.mean(older)
            
            diff = avg_recent - avg_older
            if diff > 5:
                return "Trend: Moisture increasing."
            elif diff < -5:
                return "Trend: Moisture decreasing."
        
        return "Trend: Stable."