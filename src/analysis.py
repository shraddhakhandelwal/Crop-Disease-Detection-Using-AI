"""
Data analysis module for crop disease detection system.
Provides tools for analyzing disease patterns and pesticide optimization.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path

class DiseaseAnalyzer:
    def __init__(self, log_file=None):
        """Initialize the analyzer with optional history from log file."""
        self.log_file = log_file or 'data/detection_history.csv'
        self._ensure_log_file()
        
    def _ensure_log_file(self):
        """Create log file with headers if it doesn't exist."""
        if not Path(self.log_file).exists():
            Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(columns=[
                'timestamp', 'crop_type', 'disease', 'confidence',
                'location', 'weather_conditions', 'treatment_suggested'
            ]).to_csv(self.log_file, index=False)

    def log_detection(self, crop_type, disease, confidence, location=None, 
                     weather_conditions=None, treatment=None):
        """Log a disease detection event."""
        new_row = pd.DataFrame([{
            'timestamp': datetime.now(),
            'crop_type': crop_type,
            'disease': disease,
            'confidence': confidence,
            'location': location,
            'weather_conditions': weather_conditions,
            'treatment_suggested': treatment
        }])
        new_row.to_csv(self.log_file, mode='a', header=False, index=False)

    def analyze_patterns(self, time_period='1M'):
        """Analyze disease patterns over specified time period."""
        df = pd.read_csv(self.log_file, parse_dates=['timestamp'])
        recent = df[df['timestamp'] > pd.Timestamp.now() - pd.Timedelta(time_period)]
        
        analysis = {
            'total_detections': len(recent),
            'disease_distribution': recent['disease'].value_counts().to_dict(),
            'avg_confidence': recent['confidence'].mean(),
            'crop_type_distribution': recent['crop_type'].value_counts().to_dict(),
            'detection_trend': recent.set_index('timestamp')
                                    .resample('D')['disease']
                                    .count()
                                    .to_dict()
        }
        return analysis

    def visualize_trends(self, save_path='reports/disease_trends.png'):
        """Generate visualization of disease trends."""
        df = pd.read_csv(self.log_file, parse_dates=['timestamp'])
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Disease distribution pie chart
        disease_counts = df['disease'].value_counts()
        ax1.pie(disease_counts.values, labels=disease_counts.index, autopct='%1.1f%%')
        ax1.set_title('Disease Distribution')
        
        # Detection trend line plot
        daily_counts = df.set_index('timestamp').resample('D')['disease'].count()
        sns.lineplot(data=daily_counts, ax=ax2)
        ax2.set_title('Daily Disease Detections')
        
        plt.tight_layout()
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)
        plt.close()
        
        return save_path

    def get_pesticide_recommendations(self, disease, severity):
        """Get pesticide recommendations based on disease and severity."""
        # Simplified pesticide recommendation logic
        recommendations = {
            'early_blight': {
                'low': {'pesticide': 'Copper-based fungicide', 'concentration': '0.1%'},
                'medium': {'pesticide': 'Chlorothalonil', 'concentration': '0.2%'},
                'high': {'pesticide': 'Azoxystrobin', 'concentration': '0.3%'}
            },
            'late_blight': {
                'low': {'pesticide': 'Mancozeb', 'concentration': '0.15%'},
                'medium': {'pesticide': 'Metalaxyl', 'concentration': '0.25%'},
                'high': {'pesticide': 'Cymoxanil', 'concentration': '0.35%'}
            }
        }
        
        if disease in recommendations:
            return recommendations[disease].get(severity, 
                   recommendations[disease]['medium'])
        return None

    def optimize_pesticide_usage(self, disease_history=None):
        """Optimize pesticide usage based on historical data."""
        df = pd.read_csv(self.log_file, parse_dates=['timestamp'])
        
        # Calculate disease severity trends
        severity_map = {'low': 1, 'medium': 2, 'high': 3}
        df['severity'] = df['confidence'].apply(
            lambda x: 'low' if x < 0.6 else 'medium' if x < 0.8 else 'high'
        )
        
        recommendations = {}
        for disease in df['disease'].unique():
            disease_data = df[df['disease'] == disease]
            avg_severity = disease_data['severity'].map(severity_map).mean()
            
            recommendations[disease] = {
                'suggested_treatment': self.get_pesticide_recommendations(
                    disease, 
                    'low' if avg_severity < 1.5 else 'medium' if avg_severity < 2.5 else 'high'
                ),
                'treatment_urgency': 'high' if len(disease_data) > df['disease'].value_counts().mean() else 'normal',
                'affected_crops': disease_data['crop_type'].unique().tolist()
            }
        
        return recommendations