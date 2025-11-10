"""
Enhanced visualization module with interactive plots and detailed analysis views.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json

class EnhancedVisualizer:
    def __init__(self, output_dir='reports/visualizations'):
        """Initialize visualizer with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style defaults
        plt.style.use('seaborn')
        sns.set_palette("husl")

    def create_detection_dashboard(self, detection_data, save_path=None):
        """Create an interactive dashboard of detection results."""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Disease Distribution',
                'Detection Confidence',
                'Time Series Analysis',
                'Crop Type Distribution'
            )
        )

        # Disease Distribution (Pie Chart)
        disease_counts = detection_data['disease'].value_counts()
        fig.add_trace(
            go.Pie(labels=disease_counts.index, values=disease_counts.values),
            row=1, col=1
        )

        # Detection Confidence (Box Plot)
        fig.add_trace(
            go.Box(y=detection_data['confidence'], x=detection_data['disease']),
            row=1, col=2
        )

        # Time Series
        daily_counts = detection_data.set_index('timestamp')['disease'].resample('D').count()
        fig.add_trace(
            go.Scatter(x=daily_counts.index, y=daily_counts.values),
            row=2, col=1
        )

        # Crop Distribution (Bar Chart)
        crop_counts = detection_data['crop_type'].value_counts()
        fig.add_trace(
            go.Bar(x=crop_counts.index, y=crop_counts.values),
            row=2, col=2
        )

        fig.update_layout(height=800, width=1200, title_text="Disease Detection Analysis Dashboard")
        
        if save_path:
            fig.write_html(save_path)
            return save_path
        return fig

    def create_treatment_effectiveness_plot(self, treatment_data, save_path=None):
        """Create an interactive visualization of treatment effectiveness."""
        fig = make_subplots(rows=1, cols=2,
                           subplot_titles=('Treatment Effectiveness by Disease',
                                         'Environmental Impact'))

        # Treatment effectiveness heatmap
        pivot_data = pd.pivot_table(
            treatment_data,
            values='effectiveness',
            index='treatment',
            columns='disease',
            aggfunc='mean'
        )

        fig.add_trace(
            go.Heatmap(
                z=pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                colorscale='RdYlGn'
            ),
            row=1, col=1
        )

        # Environmental impact scatter plot
        fig.add_trace(
            go.Scatter(
                x=treatment_data['environmental_factor'],
                y=treatment_data['effectiveness'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=treatment_data['concentration'],
                    colorscale='Viridis',
                    showscale=True
                ),
                text=treatment_data['disease']
            ),
            row=1, col=2
        )

        fig.update_layout(height=600, width=1200,
                         title_text="Treatment Effectiveness Analysis")

        if save_path:
            fig.write_html(save_path)
            return save_path
        return fig

    def create_severity_forecast(self, historical_data, forecast_data, save_path=None):
        """Create an interactive severity forecast visualization."""
        fig = go.Figure()

        # Historical severity
        fig.add_trace(
            go.Scatter(
                x=historical_data['timestamp'],
                y=historical_data['severity'],
                name='Historical',
                line=dict(color='blue')
            )
        )

        # Forecast
        fig.add_trace(
            go.Scatter(
                x=forecast_data['timestamp'],
                y=forecast_data['predicted_severity'],
                name='Forecast',
                line=dict(color='red', dash='dash')
            )
        )

        # Add confidence interval
        fig.add_trace(
            go.Scatter(
                x=forecast_data['timestamp'].tolist() + forecast_data['timestamp'].tolist()[::-1],
                y=forecast_data['upper_bound'].tolist() + forecast_data['lower_bound'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(231,234,241,0.5)',
                line=dict(color='rgba(231,234,241,0)'),
                name='95% Confidence Interval'
            )
        )

        fig.update_layout(
            title='Disease Severity Forecast',
            xaxis_title='Date',
            yaxis_title='Severity Index',
            hovermode='x unified'
        )

        if save_path:
            fig.write_html(save_path)
            return save_path
        return fig

    def create_geospatial_analysis(self, location_data, save_path=None):
        """Create an interactive map of disease occurrences."""
        fig = px.scatter_mapbox(
            location_data,
            lat='latitude',
            lon='longitude',
            color='disease',
            size='severity',
            hover_data=['crop_type', 'confidence', 'treatment'],
            zoom=10,
            title='Geographical Distribution of Crop Diseases'
        )

        fig.update_layout(mapbox_style='carto-positron')

        if save_path:
            fig.write_html(save_path)
            return save_path
        return fig

    def create_comparative_analysis(self, detection_results, save_path=None):
        """Create a comparative analysis of different detection methods."""
        fig = make_subplots(rows=2, cols=2,
                           specs=[[{"type": "xy"}, {"type": "polar"}],
                                 [{"type": "xy"}, {"type": "domain"}]])

        # ROC Curve
        fig.add_trace(
            go.Scatter(
                x=detection_results['fpr'],
                y=detection_results['tpr'],
                name='ROC Curve'
            ),
            row=1, col=1
        )

        # Radar Chart of Metrics
        fig.add_trace(
            go.Scatterpolar(
                r=detection_results['metrics_values'],
                theta=detection_results['metrics_names'],
                fill='toself',
                name='Model Metrics'
            ),
            row=1, col=2
        )

        # Confusion Matrix
        fig.add_trace(
            go.Heatmap(
                z=detection_results['confusion_matrix'],
                x=detection_results['class_names'],
                y=detection_results['class_names'],
                colorscale='Viridis'
            ),
            row=2, col=1
        )

        # Performance Summary
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=detection_results['overall_accuracy'],
                title={'text': "Overall Accuracy"},
                gauge={'axis': {'range': [0, 1]}}
            ),
            row=2, col=2
        )

        fig.update_layout(height=800, width=1200,
                         title_text="Model Performance Analysis")

        if save_path:
            fig.write_html(save_path)
            return save_path
        return fig