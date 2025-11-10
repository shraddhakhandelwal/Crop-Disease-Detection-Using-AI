"""
Simple Flask app to upload an image and get disease prediction.

Run:
  python src/app.py --model models/model.h5

Open http://127.0.0.1:5000
"""
import argparse
import os
import json
from flask import Flask, request, render_template, jsonify
from src.utils import preprocess_image, load_labels

app = Flask(__name__)
model = None
labels = None
img_size = 224


def try_load_model(model_path, labels_path=None):
    """Attempt to import TensorFlow and load the Keras model. Returns (model, labels) or (None, None) on failure."""
    try:
        from tensorflow.keras.models import load_model as _load_model
    except Exception as e:
        print('TensorFlow not available in this environment:', e)
        return None, None

    m = None
    l = None
    try:
        m = _load_model(model_path)
    except Exception as e:
        print('Failed to load model:', e)
        m = None
    if labels_path:
        try:
            from src.utils import load_labels as _load_labels
            l = _load_labels(labels_path)
        except Exception:
            l = None
    return m, l

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
    temp_path = os.path.join('tmp_upload.jpg')
    f.save(temp_path)
    x = preprocess_image(temp_path, target_size=(img_size, img_size))
    if model is None:
        return jsonify({'error': 'model not loaded. This server does not have TensorFlow available.'}), 500
    preds = model.predict(x)[0]
    top_idx = preds.argsort()[::-1][:3]
    results = []
    for idx in top_idx:
        label = labels.get(str(idx), labels.get(idx, str(idx))) if labels else str(idx)
        results.append({'label': label, 'score': float(preds[idx])})
    try:
        os.remove(temp_path)
    except Exception:
        pass
    return jsonify(results)


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
