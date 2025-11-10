"""
Training script for crop disease detection.

Usage example:
  python src/train.py \
    --data_dir data/train \
    --epochs 10 \
    --batch_size 32 \
    --img_size 224 \
    --model_out models/model.h5
"""
import argparse
import os
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from src.utils import save_labels


def build_transfer_model(input_shape=(224,224,3), num_classes=2, base_trainable=False):
    """Build a MobileNetV2-based classifier. If base_trainable=True the base model will be left trainable.

    Returns a compiled Keras Model (not compiled here; compilation is done in main to allow different optimizers).
    """
    base = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)
    base.trainable = base_trainable
    x = layers.GlobalAveragePooling2D()(base.output)
    x = layers.Dropout(0.3)(x)
    out = layers.Dense(num_classes, activation='softmax')(x)
    model = models.Model(inputs=base.input, outputs=out)
    return model


def main(args):
    data_dir = args.data_dir
    img_size = args.img_size
    batch_size = args.batch_size
    epochs = args.epochs
    model_out = args.model_out
    labels_out = os.path.splitext(model_out)[0] + '_labels.json'

    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        horizontal_flip=True,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        shear_range=0.05
    )

    train_gen = datagen.flow_from_directory(
        data_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    val_gen = datagen.flow_from_directory(
        data_dir,
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    num_classes = len(train_gen.class_indices)
    print('Found classes:', train_gen.class_indices)

    model = build_transfer_model(input_shape=(img_size,img_size,3), num_classes=num_classes)
    model.compile(optimizer=optimizers.Adam(learning_rate=1e-3),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    os.makedirs(os.path.dirname(model_out) or '.', exist_ok=True)

    callbacks = [
        ModelCheckpoint(model_out, monitor='val_accuracy', save_best_only=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1)
    ]

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        callbacks=callbacks
    )

    # Save labels mapping
    save_labels(train_gen.class_indices, labels_out)
    print('Saved labels mapping to', labels_out)

    # Optional fine-tuning stage: unfreeze base and continue training with a lower lr
    if args.fine_tune_epochs and args.fine_tune_epochs > 0:
        print('Starting fine-tuning stage for', args.fine_tune_epochs, 'epochs')
        # rebuild model with base trainable
        ft_model = build_transfer_model(input_shape=(img_size,img_size,3), num_classes=num_classes, base_trainable=True)
        # load weights from best checkpoint
        try:
            ft_model.load_weights(model_out)
            print('Loaded weights from', model_out)
        except Exception as e:
            print('Could not load weights for fine-tuning:', e)
        ft_model.compile(optimizer=optimizers.Adam(learning_rate=1e-4),
                         loss='categorical_crossentropy',
                         metrics=['accuracy'])

        ft_callbacks = [
            ModelCheckpoint(model_out, monitor='val_accuracy', save_best_only=True, verbose=1),
            ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1)
        ]

        ft_history = ft_model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=args.fine_tune_epochs,
            callbacks=ft_callbacks
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', required=True, help='Path to training data folder (folder-per-class)')
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--img_size', type=int, default=224)
    parser.add_argument('--model_out', default='models/model.h5')
    args = parser.parse_args()
    main(args)
