"""
Advanced pesticide optimization system with environmental consideration.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .crop_diseases import CROP_DISEASES

class PesticideOptimizer:
    def __init__(self):
        """Initialize the pesticide optimizer."""
        self.weather_impact = {
            'rain': -0.2,  # Reduce concentration if rain expected
            'high_humidity': 0.1,  # Increase for high humidity
            'wind': -0.15,  # Reduce if windy
            'hot': 0.05,  # Slight increase in hot weather
            'cold': -0.05  # Slight decrease in cold weather
        }
        
        self.soil_impact = {
            'sandy': 0.1,  # Increase for sandy soil (faster drainage)
            'clay': -0.1,  # Decrease for clay soil (slower drainage)
            'loamy': 0,    # Neutral for loamy soil
            'acidic': 0.05,  # Slight increase for acidic soil
            'alkaline': -0.05  # Slight decrease for alkaline soil
        }

    def _parse_weather(self, weather_str):
        """Parse weather string to identify conditions."""
        weather_str = weather_str.lower()
        conditions = []
        
        if any(x in weather_str for x in ['rain', 'shower', 'drizzle']):
            conditions.append('rain')
        if any(x in weather_str for x in ['humid', 'muggy']):
            conditions.append('high_humidity')
        if any(x in weather_str for x in ['wind', 'breezy', 'gusty']):
            conditions.append('wind')
        if any(x in weather_str for x in ['hot', 'warm', 'heat']):
            conditions.append('hot')
        if any(x in weather_str for x in ['cold', 'cool', 'chill']):
            conditions.append('cold')
            
        return conditions

    def get_environmental_factor(self, weather_str, soil_type='loamy'):
        """Calculate environmental adjustment factor."""
        conditions = self._parse_weather(weather_str)
        
        # Calculate weather impact
        weather_factor = sum(self.weather_impact.get(cond, 0) for cond in conditions)
        
        # Add soil impact
        soil_factor = self.soil_impact.get(soil_type, 0)
        
        # Combine factors (ensuring result stays within reasonable bounds)
        total_factor = 1 + weather_factor + soil_factor
        return max(0.5, min(1.5, total_factor))

    def optimize_treatment(self, crop_type, disease, severity, weather=None, soil_type='loamy'):
        """Get optimized treatment recommendation."""
        if crop_type not in CROP_DISEASES or disease not in CROP_DISEASES[crop_type]:
            return None

        # Get base treatment
        base_treatment = CROP_DISEASES[crop_type][disease]['treatments'][severity]
        
        if not weather:
            return base_treatment

        # Apply environmental adjustments
        env_factor = self.get_environmental_factor(weather, soil_type)
        
        # Adjust concentration
        base_conc = float(base_treatment['concentration'].strip('%')) / 100
        adjusted_conc = base_conc * env_factor
        
        return {
            'pesticide': base_treatment['pesticide'],
            'concentration': f"{adjusted_conc:.3%}",
            'environmental_factor': env_factor,
            'weather_conditions': weather,
            'soil_type': soil_type,
            'notes': self._generate_application_notes(weather, env_factor)
        }

    def _generate_application_notes(self, weather, env_factor):
        """Generate application notes based on conditions."""
        notes = []
        weather_lower = weather.lower()
        
        if 'rain' in weather_lower:
            notes.append("Wait for dry conditions if possible")
        if 'wind' in weather_lower:
            notes.append("Apply in early morning or evening to minimize drift")
        if env_factor > 1.1:
            notes.append("Environmental conditions require increased concentration")
        elif env_factor < 0.9:
            notes.append("Environmental conditions allow reduced concentration")
        
        return notes if notes else ["Standard application conditions"]

    def calculate_reapplication_interval(self, weather_forecast, base_interval=14):
        """Calculate when to reapply based on weather forecast."""
        conditions = [self._parse_weather(w) for w in weather_forecast]
        
        # Adjust interval based on conditions
        interval = base_interval
        
        for day_conditions in conditions:
            if 'rain' in day_conditions:
                interval -= 1
            if 'high_humidity' in day_conditions:
                interval -= 0.5
            
        # Ensure minimum interval of 7 days
        return max(7, int(interval))