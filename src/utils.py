import json
from PIL import Image
import numpy as np
import os


def preprocess_image(image_path, target_size=(224, 224)):
    """Load an image file and preprocess to model input.

    Returns: numpy array of shape (1, H, W, C) float32 normalized to [0,1]
    """
    img = Image.open(image_path).convert('RGB')
    img = img.resize(target_size)
    arr = np.array(img).astype('float32') / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr


def save_labels(mapping, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)


def load_labels(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
