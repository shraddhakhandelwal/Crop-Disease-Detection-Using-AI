"""
Visualization module for crop disease detection system.
Provides tools for visualizing disease patterns and analysis results.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import cv2

class DiseaseVisualizer:
    def __init__(self, output_dir='reports/visualizations'):
        """Initialize visualizer with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def visualize_detection(self, image_path, predictions, save_path=None):
        """
        Visualize disease detection results on the image.
        
        Args:
            image_path: Path to the original image
            predictions: List of dictionaries with 'label' and 'score' keys
            save_path: Optional path to save the visualization
        """
        # Read and resize image
        img = cv2.imread(str(image_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Create figure
        plt.figure(figsize=(12, 6))
        
        # Plot original image
        plt.subplot(1, 2, 1)
        plt.imshow(img)
        plt.title('Original Image')
        plt.axis('off')
        
        # Plot prediction confidence
        plt.subplot(1, 2, 2)
        labels = [p['label'] for p in predictions]
        scores = [p['score'] for p in predictions]
        
        colors = sns.color_palette('husl', n_colors=len(predictions))
        bars = plt.barh(labels, scores, color=colors)
        plt.title('Disease Detection Confidence')
        plt.xlim(0, 1)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2,
                    f'{width:.2%}', ha='left', va='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return save_path
        else:
            return plt.gcf()

    def plot_confidence_heatmap(self, disease_data, save_path=None):
        """Create a heatmap of detection confidence by crop and disease type."""
        pivot_data = disease_data.pivot_table(
            values='confidence',
            index='crop_type',
            columns='disease',
            aggfunc='mean'
        )
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(pivot_data, annot=True, fmt='.2%', cmap='YlOrRd')
        plt.title('Disease Detection Confidence by Crop Type')
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return save_path
        else:
            return plt.gcf()

    def create_severity_map(self, location_data, save_path=None):
        """Create a geographical visualization of disease severity."""
        plt.figure(figsize=(12, 8))
        
        # Create scatter plot of disease occurrences
        scatter = plt.scatter(
            location_data['longitude'],
            location_data['latitude'],
            c=location_data['severity'],
            cmap='YlOrRd',
            s=100,
            alpha=0.6
        )
        
        plt.colorbar(scatter, label='Disease Severity')
        plt.title('Geographical Distribution of Disease Severity')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return save_path
        else:
            return plt.gcf()

    def plot_treatment_effectiveness(self, treatment_data, save_path=None):
        """Visualize the effectiveness of different treatments."""
        plt.figure(figsize=(12, 6))
        
        sns.boxplot(
            x='treatment_type',
            y='effectiveness_score',
            hue='disease',
            data=treatment_data
        )
        
        plt.title('Treatment Effectiveness by Disease Type')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return save_path
        else:
            return plt.gcf()

    def generate_report(self, analyzer, time_period='1M'):
        """Generate a comprehensive visual report."""
        analysis = analyzer.analyze_patterns(time_period)
        
        # Create report directory
        report_path = self.output_dir / f'report_{datetime.now().strftime("%Y%m%d")}'
        report_path.mkdir(exist_ok=True)
        
        # Disease distribution
        plt.figure(figsize=(10, 6))
        plt.pie(
            analysis['disease_distribution'].values(),
            labels=analysis['disease_distribution'].keys(),
            autopct='%1.1f%%'
        )
        plt.title('Disease Distribution')
        plt.savefig(report_path / 'disease_distribution.png')
        plt.close()
        
        # Detection trend
        plt.figure(figsize=(12, 6))
        dates = list(analysis['detection_trend'].keys())
        counts = list(analysis['detection_trend'].values())
        plt.plot(dates, counts)
        plt.title('Disease Detection Trend')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(report_path / 'detection_trend.png')
        plt.close()
        
        return report_path