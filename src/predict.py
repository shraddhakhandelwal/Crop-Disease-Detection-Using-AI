"""
Predict a single image using a trained model.

Usage:
  python src/predict.py --model models/model.h5 --image examples/sample_leaf.jpg
"""
import argparse
import os
import json
import numpy as np
from tensorflow.keras.models import load_model
from src.utils import preprocess_image, load_labels


def predict_single(model_path, image_path, labels_path=None, top_k=3, img_size=224):
    model = load_model(model_path)
    x = preprocess_image(image_path, target_size=(img_size, img_size))
    preds = model.predict(x)[0]
    top_idx = np.argsort(preds)[::-1][:top_k]

    labels = None
    if labels_path and os.path.exists(labels_path):
        labels = load_labels(labels_path)
        # invert mapping if necessary
        if labels and isinstance(next(iter(labels.values())), int):
            inv = {v: k for k, v in labels.items()}
        else:
            inv = labels
    else:
        inv = None

    results = []
    for idx in top_idx:
        label = inv.get(str(idx), inv.get(idx, str(idx))) if inv else str(idx)
        results.append({'label': label, 'score': float(preds[idx])})
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--image', required=True)
    parser.add_argument('--labels', default=None, help='Optional labels json saved by train script')
    parser.add_argument('--top_k', type=int, default=3)
    parser.add_argument('--img_size', type=int, default=224)
    args = parser.parse_args()
    res = predict_single(args.model, args.image, labels_path=args.labels, top_k=args.top_k, img_size=args.img_size)
    print(json.dumps(res, indent=2))
