"""
MoodMate - Emotion Detection Model Architecture
================================================
CNN model for facial emotion detection using FER-2013 dataset.
Saved in modern .keras format (recommended over legacy .h5)

Usage:
  python emotion_model.py              # Build + show summary
  python emotion_model.py --train      # Train on FER-2013 and save model
  python emotion_model.py --predict    # Test prediction on a sample image
"""

import os
import sys
import numpy as np

# ── Try importing Keras/TensorFlow ────────────────────────────────────────────
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models, callbacks
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    KERAS_AVAILABLE = True
    print(f"✅ TensorFlow {tf.__version__} / Keras loaded")
except ImportError:
    try:
        import tf_keras as keras
        from tf_keras import layers, models, callbacks
        from tf_keras.preprocessing.image import ImageDataGenerator
        KERAS_AVAILABLE = True
        print("✅ tf-keras loaded")
    except ImportError:
        KERAS_AVAILABLE = False
        print("⚠️  Install TensorFlow: pip install tensorflow")

# ── Constants ─────────────────────────────────────────────────────────────────
EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
NUM_CLASSES    = len(EMOTION_LABELS)
IMAGE_SIZE     = (48, 48)
MODEL_PATH     = os.path.join(os.path.dirname(__file__), 'emotion_model.keras')


# ── Model Architecture ────────────────────────────────────────────────────────
def build_emotion_model():
    """
    CNN architecture for FER-2013 emotion classification.

    Architecture summary:
      Input: 48x48 grayscale face image
        ↓
      Block 1: Conv2D(64) → Conv2D(64) → MaxPool → BatchNorm → Dropout(0.25)
        ↓
      Block 2: Conv2D(128) → Conv2D(128) → MaxPool → BatchNorm → Dropout(0.25)
        ↓
      Block 3: Conv2D(256) → MaxPool → BatchNorm → Dropout(0.25)
        ↓
      Flatten → Dense(1024, ReLU) → Dropout(0.5) → Dense(7, Softmax)
        ↓
      Output: probability across 7 emotion classes
    """
    if not KERAS_AVAILABLE:
        print("❌ Keras not available")
        return None

    model = models.Sequential(name='moodmate_emotion_cnn')

    # ── Input ──────────────────────────────────────────────────────────────
    model.add(layers.Input(shape=(48, 48, 1), name='face_input'))

    # ── Block 1: 64 filters ────────────────────────────────────────────────
    model.add(layers.Conv2D(64, (3,3), padding='same', activation='relu', name='conv1_1'))
    model.add(layers.Conv2D(64, (3,3), padding='same', activation='relu', name='conv1_2'))
    model.add(layers.MaxPooling2D((2,2), name='pool1'))
    model.add(layers.BatchNormalization(name='bn1'))
    model.add(layers.Dropout(0.25, name='drop1'))

    # ── Block 2: 128 filters ───────────────────────────────────────────────
    model.add(layers.Conv2D(128, (3,3), padding='same', activation='relu', name='conv2_1'))
    model.add(layers.Conv2D(128, (3,3), padding='same', activation='relu', name='conv2_2'))
    model.add(layers.MaxPooling2D((2,2), name='pool2'))
    model.add(layers.BatchNormalization(name='bn2'))
    model.add(layers.Dropout(0.25, name='drop2'))

    # ── Block 3: 256 filters ───────────────────────────────────────────────
    model.add(layers.Conv2D(256, (3,3), padding='same', activation='relu', name='conv3_1'))
    model.add(layers.MaxPooling2D((2,2), name='pool3'))
    model.add(layers.BatchNormalization(name='bn3'))
    model.add(layers.Dropout(0.25, name='drop3'))

    # ── Classifier ─────────────────────────────────────────────────────────
    model.add(layers.Flatten(name='flatten'))
    model.add(layers.Dense(1024, activation='relu', name='fc1'))
    model.add(layers.Dropout(0.5, name='drop_fc'))
    model.add(layers.Dense(NUM_CLASSES, activation='softmax', name='emotion_output'))

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


# ── Save model ────────────────────────────────────────────────────────────────
def save_model(model, path=MODEL_PATH):
    """
    Save model in modern .keras format.
    The .keras format is the recommended format from TensorFlow 2.12+
    It replaces the legacy .h5 format and stores:
      - Model architecture
      - Weights
      - Optimizer state
      - Training config
    """
    model.save(path)
    size_mb = os.path.getsize(path) / (1024 * 1024)
    print(f"✅ Model saved: {path}  ({size_mb:.1f} MB)")
    print(f"   Format: .keras  (modern format, replaces legacy .h5)")


# ── Load model ────────────────────────────────────────────────────────────────
def load_model(path=MODEL_PATH):
    """Load the saved .keras model."""
    if not os.path.exists(path):
        print(f"❌ Model not found at: {path}")
        print("   Run: python emotion_model.py --train")
        return None
    model = keras.models.load_model(path)
    print(f"✅ Loaded model: {path}")
    return model


# ── Train model ───────────────────────────────────────────────────────────────
def train_model(data_dir='data/fer2013'):
    """
    Train the emotion CNN on FER-2013 dataset.

    Expected folder structure:
      data/fer2013/
        train/
          angry/    sad/    happy/   ...
        test/
          angry/    sad/    happy/   ...

    Download FER-2013 from:
      https://www.kaggle.com/datasets/msambare/fer2013
    """
    if not KERAS_AVAILABLE:
        return None

    train_dir = os.path.join(data_dir, 'train')
    test_dir  = os.path.join(data_dir, 'test')

    if not os.path.exists(train_dir):
        print(f"❌ Training data not found at: {train_dir}")
        print("   Download FER-2013 from: https://www.kaggle.com/datasets/msambare/fer2013")
        print("   Unzip into: data/fer2013/")
        return None

    print("📦 Loading FER-2013 dataset...")

    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.1,
    )
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_gen = train_datagen.flow_from_directory(
        train_dir,
        target_size=IMAGE_SIZE,
        color_mode='grayscale',
        batch_size=64,
        class_mode='categorical',
        shuffle=True,
    )
    test_gen = test_datagen.flow_from_directory(
        test_dir,
        target_size=IMAGE_SIZE,
        color_mode='grayscale',
        batch_size=64,
        class_mode='categorical',
        shuffle=False,
    )

    print(f"✅ Classes found: {train_gen.class_indices}")
    print(f"   Training samples: {train_gen.samples}")
    print(f"   Test samples:     {test_gen.samples}")

    # Build model
    model = build_emotion_model()

    # Callbacks
    cbs = [
        callbacks.EarlyStopping(
            monitor='val_accuracy', patience=10,
            restore_best_weights=True, verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.5,
            patience=5, min_lr=1e-6, verbose=1
        ),
        callbacks.ModelCheckpoint(
            MODEL_PATH, monitor='val_accuracy',
            save_best_only=True, verbose=1
        ),
    ]

    print("\n🚀 Training started...")
    history = model.fit(
        train_gen,
        epochs=60,
        validation_data=test_gen,
        callbacks=cbs,
        verbose=1,
    )

    # Final evaluation
    loss, acc = model.evaluate(test_gen, verbose=0)
    print(f"\n✅ Training complete!")
    print(f"   Test accuracy: {acc*100:.2f}%")
    print(f"   Test loss:     {loss:.4f}")

    # Save in .keras format
    save_model(model)
    return model, history


# ── Predict emotion ───────────────────────────────────────────────────────────
def predict_emotion(model, image_array):
    """
    Predict emotion from a preprocessed face image.

    Args:
        model:       Loaded Keras model
        image_array: numpy array shape (48,48) or (48,48,1), uint8 0-255

    Returns:
        dict: { emotion, confidence, scores }
    """
    if model is None:
        return None

    img = image_array.astype('float32') / 255.0
    if img.ndim == 2:
        img = np.expand_dims(img, axis=-1)   # (48,48) → (48,48,1)
    img = np.expand_dims(img, axis=0)         # → (1,48,48,1)

    preds      = model.predict(img, verbose=0)[0]
    scores     = {label: round(float(p), 4) for label, p in zip(EMOTION_LABELS, preds)}
    top_idx    = int(np.argmax(preds))

    return {
        'emotion':    EMOTION_LABELS[top_idx],
        'confidence': round(float(preds[top_idx]), 4),
        'scores':     scores
    }


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if '--train' in sys.argv:
        # Train from scratch on FER-2013
        train_model()

    elif '--predict' in sys.argv:
        # Load model and test on a random noise image
        model = load_model()
        if model:
            dummy_face = np.random.randint(0, 255, (48, 48), dtype=np.uint8)
            result     = predict_emotion(model, dummy_face)
            print(f"\nSample prediction: {result}")

    else:
        # Default: build and show model summary
        print("\n" + "="*55)
        print("  MoodMate — Emotion Detection CNN Architecture")
        print("="*55)
        model = build_emotion_model()
        if model:
            model.summary()
            print(f"\n📊 Total parameters : {model.count_params():,}")
            print(f"📥 Input  shape     : (batch, 48, 48, 1)")
            print(f"📤 Output shape     : (batch, {NUM_CLASSES})")
            print(f"🏷️  Emotion classes  : {EMOTION_LABELS}")
            print(f"💾 Save format      : .keras  (modern, replaces .h5)")
            print(f"💾 Save path        : {MODEL_PATH}")
            print("\nTo train:   python emotion_model.py --train")
            print("To predict: python emotion_model.py --predict")
