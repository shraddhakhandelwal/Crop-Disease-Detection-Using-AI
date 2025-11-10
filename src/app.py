"""
Advanced Flask application for crop disease detection and analysis.

Features:
- Disease detection from images
- Historical pattern analysis
- Pesticide optimization
- Visualization tools

Run:
  python src/app.py --model models/model.h5

Open http://127.0.0.1:5000
"""
import argparse
import os
import json
from flask import Flask, request, render_template, jsonify, send_file
from tensorflow.keras.models import load_model
from src.utils import preprocess_image, load_labels
from src.analysis import DiseaseAnalyzer
from src.visualization import DiseaseVisualizer
import os
from datetime import datetime

app = Flask(__name__)
model = None
labels = None
img_size = 224
analyzer = DiseaseAnalyzer()
visualizer = DiseaseVisualizer()

# The HTML UI was moved into templates/index.html for cleaner structure


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'no file uploaded'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'empty filename'}), 400
        
    # Process image and get predictions
    temp_path = os.path.join('tmp_upload.jpg')
    f.save(temp_path)
    x = preprocess_image(temp_path, target_size=(img_size, img_size))
    preds = model.predict(x)[0]
    top_idx = preds.argsort()[::-1][:3]
    
    results = []
    for idx in top_idx:
        label = labels.get(str(idx), labels.get(idx, str(idx))) if labels else str(idx)
        confidence = float(preds[idx])
        results.append({'label': label, 'score': confidence})
        
        # Log detection for analysis
        if confidence > 0.5:  # Only log significant detections
            analyzer.log_detection(
                crop_type=request.form.get('crop_type', 'unknown'),
                disease=label,
                confidence=confidence,
                location=request.form.get('location'),
                weather_conditions=request.form.get('weather')
            )
    
    # Generate visualization
    viz_path = os.path.join('reports', 'visualizations', f'detection_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
    visualizer.visualize_detection(temp_path, results, viz_path)
    
    # Get pesticide recommendations
    if results:
        top_disease = results[0]
        severity = 'low' if top_disease['score'] < 0.6 else 'medium' if top_disease['score'] < 0.8 else 'high'
        pesticide_rec = analyzer.get_pesticide_recommendations(top_disease['label'], severity)
        if pesticide_rec:
            results[0]['treatment'] = pesticide_rec
    
    try:
        os.remove(temp_path)
    except Exception:
        pass
        
    return jsonify({
        'predictions': results,
        'visualization': viz_path
    })

@app.route('/analysis', methods=['GET'])
def get_analysis():
    time_period = request.args.get('period', '1M')
    analysis = analyzer.analyze_patterns(time_period)
    return jsonify(analysis)

@app.route('/visualizations/<path:filename>')
def get_visualization(filename):
    return send_file(os.path.join('reports', 'visualizations', filename))

@app.route('/report', methods=['GET'])
def get_report():
    # Generate comprehensive report
    report_path = visualizer.generate_report(analyzer)
    analysis = analyzer.analyze_patterns('1M')
    recommendations = analyzer.optimize_pesticide_usage()
    
    return jsonify({
        'analysis': analysis,
        'pesticide_recommendations': recommendations,
        'report_files': [str(p) for p in report_path.glob('*.png')]
    })


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--labels', default=None)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    model = load_model(args.model)
    labels = load_labels(args.labels) if args.labels else None
    app.run(host=args.host, port=args.port, debug=True)
