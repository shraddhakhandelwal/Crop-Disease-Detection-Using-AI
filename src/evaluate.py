"""
Evaluate a trained model on a directory with folder-per-class images.

Usage:
  python src/evaluate.py --model models/model.h5 --data_dir data/val --img_size 224
"""
import argparse
import os
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def evaluate(model_path, data_dir, img_size=224, batch_size=32):
    model = load_model(model_path)
    datagen = ImageDataGenerator(rescale=1./255)
    gen = datagen.flow_from_directory(
        data_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )
    steps = int(np.ceil(gen.samples / batch_size))
    preds = model.predict(gen, steps=steps)
    y_pred = np.argmax(preds, axis=1)
    y_true = gen.classes
    labels = list(gen.class_indices.keys())

    print('Classification Report:')
    print(classification_report(y_true, y_pred, target_names=labels))
    print('Confusion Matrix:')
    print(confusion_matrix(y_true, y_pred))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    parser.add_argument('--data_dir', required=True, help='directory with folder-per-class images')
    parser.add_argument('--img_size', type=int, default=224)
    parser.add_argument('--batch_size', type=int, default=32)
    args = parser.parse_args()
    evaluate(args.model, args.data_dir, img_size=args.img_size, batch_size=args.batch_size)
