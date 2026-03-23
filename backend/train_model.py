"""
CNN Model Training Script for Facial Emotion Detection
Uses MobileNetV2 Transfer Learning on FER-2013 Dataset

Emotions: angry, happy, neutral, sad, surprise (5 classes)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
from keras import layers, models, callbacks, optimizers
from keras.applications import MobileNetV2
from keras.utils import to_categorical


# ─── Configuration ────────────────────────────────────────────────────────────

EMOTION_LABELS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
TARGET_EMOTIONS = {"angry": 0, "happy": 1, "neutral": 2, "sad": 3, "surprise": 4}
TARGET_LABELS = list(TARGET_EMOTIONS.keys())

# Mapping from FER-2013 7-class to our 5-class
# disgust → angry, fear → sad (closest mapping)
FER_TO_TARGET = {
    0: 0,   # angry → angry
    1: 0,   # disgust → angry
    2: 3,   # fear → sad
    3: 1,   # happy → happy
    4: 3,   # sad → sad
    5: 4,   # surprise → surprise
    6: 2,   # neutral → neutral
}

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20
MODEL_SAVE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "model.keras")


# ─── Data Loading ─────────────────────────────────────────────────────────────

def load_fer2013(csv_path=None):
    """
    Load FER-2013 dataset. Downloads if needed.
    FER-2013 format: emotion, pixels (space-separated), Usage
    """
    if csv_path and os.path.exists(csv_path):
        print(f"[INFO] Loading FER-2013 from: {csv_path}")
        df = pd.read_csv(csv_path)
    else:
        # Try to load from kaggle datasets
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        local_path = os.path.join(data_dir, "fer2013.csv")

        if os.path.exists(local_path):
            print(f"[INFO] Loading FER-2013 from: {local_path}")
            df = pd.read_csv(local_path)
        else:
            print("[INFO] FER-2013 not found locally. Attempting download via kagglehub...")
            try:
                import kagglehub
                path = kagglehub.dataset_download("msambare/fer2013")
                print(f"[INFO] Dataset downloaded to: {path}")
                # Find the CSV file
                for root, dirs, files in os.walk(path):
                    for f in files:
                        if f.endswith(".csv"):
                            local_path = os.path.join(root, f)
                            break
                df = pd.read_csv(local_path)
            except ImportError:
                print("[ERROR] kagglehub not installed. Install with: pip install kagglehub")
                print("[INFO] Alternatively, download FER-2013 manually from:")
                print("       https://www.kaggle.com/datasets/msambare/fer2013")
                print(f"       Place fer2013.csv in: {data_dir}")
                raise FileNotFoundError(
                    "FER-2013 dataset not found. Please download it manually."
                )

    return df


def preprocess_data(df):
    """
    Convert FER-2013 pixels to images and map to 5 target emotions.
    """
    print("[INFO] Preprocessing data...")

    pixels = df["pixels"].values
    emotions = df["emotion"].values

    images = []
    labels = []

    for i, (pixel_str, emotion) in enumerate(zip(pixels, emotions)):
        if emotion not in FER_TO_TARGET:
            continue

        # Parse pixel string to numpy array (48x48 grayscale)
        pixel_array = np.array(pixel_str.split(), dtype=np.uint8).reshape(48, 48)

        # Convert grayscale to RGB by stacking
        rgb_image = np.stack([pixel_array] * 3, axis=-1)

        # Resize to MobileNet input size (224x224)
        rgb_image = tf.image.resize(rgb_image, (IMG_SIZE, IMG_SIZE)).numpy().astype(np.uint8)

        images.append(rgb_image)
        labels.append(FER_TO_TARGET[emotion])

        if (i + 1) % 5000 == 0:
            print(f"  Processed {i + 1}/{len(pixels)} images...")

    images = np.array(images, dtype=np.float32)
    labels = np.array(labels, dtype=np.int32)

    # Normalize to [0, 1]
    images = images / 255.0

    # One-hot encode labels
    labels_onehot = to_categorical(labels, num_classes=len(TARGET_LABELS))

    print(f"[INFO] Dataset: {len(images)} images across {len(TARGET_LABELS)} classes")

    # Print class distribution
    unique, counts = np.unique(labels, return_counts=True)
    for u, c in zip(unique, counts):
        print(f"  {TARGET_LABELS[u]}: {c} samples")

    return images, labels_onehot


# ─── Model Architecture ──────────────────────────────────────────────────────

def build_model():
    """
    Build CNN model using MobileNetV2 transfer learning.
    - Base: MobileNetV2 pretrained on ImageNet (frozen)
    - Head: GlobalAveragePooling → Dense(256) → Dropout → Dense(128) → Dropout → Dense(5, softmax)
    """
    print("[INFO] Building MobileNetV2 transfer learning model...")

    # Load MobileNetV2 base (without top classification layers)
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )

    # Freeze base model layers
    base_model.trainable = False

    # Build classification head
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(len(TARGET_LABELS), activation="softmax"),
    ])

    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()
    return model, base_model


def fine_tune_model(model, base_model, X_train, y_train, X_val, y_val):
    """
    Fine-tune the model in two phases:
    Phase 1: Train only the classification head (base frozen)
    Phase 2: Unfreeze top layers of MobileNet and fine-tune
    """
    # ─── Phase 1: Train classification head ───────────────────────────────

    print("\n" + "=" * 60)
    print("PHASE 1: Training classification head (base frozen)")
    print("=" * 60)

    cb_list = [
        callbacks.EarlyStopping(
            monitor="val_accuracy", patience=5, restore_best_weights=True
        ),
        callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6
        ),
    ]

    history1 = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=cb_list,
        verbose=1,
    )

    # ─── Phase 2: Fine-tune top MobileNet layers ─────────────────────────

    print("\n" + "=" * 60)
    print("PHASE 2: Fine-tuning top MobileNet layers")
    print("=" * 60)

    # Unfreeze top 30 layers of MobileNet
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    # Recompile with lower learning rate
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    cb_list_ft = [
        callbacks.EarlyStopping(
            monitor="val_accuracy", patience=5, restore_best_weights=True
        ),
        callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=3, min_lr=1e-7
        ),
    ]

    history2 = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=cb_list_ft,
        verbose=1,
    )

    return model, history1, history2


# ─── Plotting ─────────────────────────────────────────────────────────────────

def plot_training_history(history1, history2, save_path=None):
    """Plot training and validation accuracy/loss curves."""
    # Combine histories
    acc = history1.history["accuracy"] + history2.history["accuracy"]
    val_acc = history1.history["val_accuracy"] + history2.history["val_accuracy"]
    loss = history1.history["loss"] + history2.history["loss"]
    val_loss = history1.history["val_loss"] + history2.history["val_loss"]

    epochs_range = range(1, len(acc) + 1)
    phase1_epochs = len(history1.history["accuracy"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Accuracy
    ax1.plot(epochs_range, acc, "b-", label="Training Accuracy")
    ax1.plot(epochs_range, val_acc, "r-", label="Validation Accuracy")
    ax1.axvline(x=phase1_epochs, color="gray", linestyle="--", label="Fine-tuning start")
    ax1.set_title("Model Accuracy")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Loss
    ax2.plot(epochs_range, loss, "b-", label="Training Loss")
    ax2.plot(epochs_range, val_loss, "r-", label="Validation Loss")
    ax2.axvline(x=phase1_epochs, color="gray", linestyle="--", label="Fine-tuning start")
    ax2.set_title("Model Loss")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Loss")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"[INFO] Training plot saved to: {save_path}")
    else:
        plt.show()


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Emotion Detection CNN — MobileNetV2 Transfer Learning")
    print("  Training on FER-2013 Dataset")
    print("=" * 60)

    # Ensure models directory exists
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

    # Load data
    df = load_fer2013()

    # Preprocess
    images, labels = preprocess_data(df)

    # Split into train/validation/test
    X_train, X_test, y_train, y_test = train_test_split(
        images, labels, test_size=0.15, random_state=42, stratify=labels.argmax(axis=1)
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.15, random_state=42, stratify=y_train.argmax(axis=1)
    )

    print(f"\n[INFO] Data splits:")
    print(f"  Training:   {len(X_train)} samples")
    print(f"  Validation: {len(X_val)} samples")
    print(f"  Test:       {len(X_test)} samples")

    # Build model
    model, base_model = build_model()

    # Train
    model, history1, history2 = fine_tune_model(
        model, base_model, X_train, y_train, X_val, y_val
    )

    # Evaluate on test set
    print("\n" + "=" * 60)
    print("EVALUATION on Test Set")
    print("=" * 60)

    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=1)
    print(f"\n  Test Accuracy: {test_acc:.4f}")
    print(f"  Test Loss:     {test_loss:.4f}")

    # Save model
    model.save(MODEL_SAVE_PATH)
    print(f"\n[INFO] Model saved to: {MODEL_SAVE_PATH}")

    # Plot training history
    plot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    plot_path = os.path.join(plot_dir, "training_history.png")
    plot_training_history(history1, history2, save_path=plot_path)

    # Print classification report
    from sklearn.metrics import classification_report
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)

    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)
    print(classification_report(y_true_classes, y_pred_classes, target_names=TARGET_LABELS))

    print("\n[DONE] Training complete!")
    print(f"Model saved at: {MODEL_SAVE_PATH}")


if __name__ == "__main__":
    main()
