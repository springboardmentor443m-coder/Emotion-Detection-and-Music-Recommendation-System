"""
CNN-based Facial Emotion Detection Module

Loads the trained MobileNetV2 model weights and performs
facial emotion detection from uploaded images.

Rebuilds model architecture locally to avoid Keras version
mismatch issues between training (Kaggle) and inference (local).

Supported emotions: angry, happy, neutral, sad, surprise
"""

import os
import io
import zipfile
import tempfile
import numpy as np
from PIL import Image

# Suppress TF warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# ─── Configuration ────────────────────────────────────────────────────────────

TARGET_LABELS = ["angry", "happy", "neutral", "sad", "surprise"]
IMG_SIZE = 96
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "model.keras")

# ─── Model Building & Loading ─────────────────────────────────────────────────

_model = None
_face_cascade = None


def _build_model():
    """
    Rebuild the exact same model architecture used during training.
    Uses Functional API to avoid Sequential + BatchNormalization issues.
    """
    import tensorflow as tf
    from keras import layers, models
    from keras.applications import MobileNetV2

    # Same architecture as train_model.py
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )

    # Use Functional API instead of Sequential to avoid BN issues
    inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(len(TARGET_LABELS), activation="softmax")(x)

    model = models.Model(inputs, outputs)
    return model


def _get_model():
    """Load the trained CNN model by rebuilding architecture and loading weights."""
    global _model
    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Trained model not found at: {MODEL_PATH}\n"
            "Please place model.keras in the models/ folder."
        )

    print(f"[INFO] Loading CNN model from: {MODEL_PATH}")

    # Build the model architecture locally
    print("[INFO] Rebuilding model architecture...")
    model = _build_model()

    # Extract weights from the .keras file (it's a zip archive)
    print("[INFO] Extracting and loading weights...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        with zipfile.ZipFile(MODEL_PATH, "r") as z:
            z.extractall(tmp_dir)

        # Find the weights file inside the extracted archive
        weights_file = None
        for root, dirs, files in os.walk(tmp_dir):
            for f in files:
                if f.endswith(".h5") or f.endswith(".weights.h5"):
                    weights_file = os.path.join(root, f)
                    break
            if weights_file:
                break

        if weights_file:
            try:
                model.load_weights(weights_file)
                print(f"[INFO] Weights loaded from: {os.path.basename(weights_file)}")
            except Exception as e:
                print(f"[WARN] Exact weight loading failed: {e}")
                print("[INFO] Trying with skip_mismatch=True...")
                model.load_weights(weights_file, skip_mismatch=True)
                print("[INFO] Weights loaded with skip_mismatch=True")
        else:
            # If no .h5 found, try loading weights directly from .keras
            try:
                model.load_weights(MODEL_PATH)
                print("[INFO] Weights loaded directly from .keras file")
            except Exception as e:
                print(f"[WARN] Direct weight loading failed: {e}")
                print("[INFO] Trying load_weights with skip_mismatch...")
                model.load_weights(MODEL_PATH, skip_mismatch=True)

    _model = model
    print("[INFO] CNN model ready for inference.")
    return _model


def _get_face_cascade():
    """Load the Haar Cascade face detector."""
    global _face_cascade
    if _face_cascade is not None:
        return _face_cascade

    try:
        import cv2
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        _face_cascade = cv2.CascadeClassifier(cascade_path)
        if _face_cascade.empty():
            print("[WARN] Haar cascade is empty, face detection disabled")
            _face_cascade = None
    except Exception as e:
        print(f"[WARN] Could not load face cascade: {e}")
        _face_cascade = None

    return _face_cascade


# ─── Face Detection ───────────────────────────────────────────────────────────

def detect_faces(pil_image):
    """Detect faces using Haar Cascade. Returns list of (x,y,w,h)."""
    cascade = _get_face_cascade()
    if cascade is None:
        return []

    try:
        import cv2
        img_array = np.array(pil_image)
        if len(img_array.shape) == 2:
            gray = img_array
        else:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces if len(faces) > 0 else []
    except Exception as e:
        print(f"[WARN] Face detection failed: {e}")
        return []


# ─── Emotion Detection ────────────────────────────────────────────────────────

def detect_emotion_from_image(image_bytes: bytes) -> dict:
    """
    Detect emotion from a facial image.

    Args:
        image_bytes: Raw image bytes (JPEG/PNG)

    Returns:
        dict with emotion, confidence, all_scores, face_detected
    """
    model = _get_model()

    # Open image
    pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Face detection
    faces = detect_faces(pil_image)
    face_detected = len(faces) > 0

    if face_detected:
        # Use the largest face
        if len(faces) > 1:
            areas = [w * h for (x, y, w, h) in faces]
            best_idx = np.argmax(areas)
            bbox = tuple(faces[best_idx])
        else:
            bbox = tuple(faces[0])

        # Crop face with margin
        x, y, w, h = bbox
        margin = int(0.15 * max(w, h))
        img_w, img_h = pil_image.size
        x1, y1 = max(0, x - margin), max(0, y - margin)
        x2, y2 = min(img_w, x + w + margin), min(img_h, y + h + margin)
        face_image = pil_image.crop((x1, y1, x2, y2))
    else:
        face_image = pil_image

    # Preprocess
    face_resized = face_image.resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS)
    face_array = np.array(face_resized, dtype=np.float32) / 255.0

    if len(face_array.shape) == 2:
        face_array = np.stack([face_array] * 3, axis=-1)
    elif face_array.shape[2] == 4:
        face_array = face_array[:, :, :3]

    face_batch = np.expand_dims(face_array, axis=0)

    # Predict
    predictions = model.predict(face_batch, verbose=0)[0]

    emotion_scores = {TARGET_LABELS[i]: float(predictions[i]) for i in range(len(TARGET_LABELS))}
    top_emotion = max(emotion_scores, key=emotion_scores.get)

    return {
        "emotion": top_emotion,
        "confidence": round(emotion_scores[top_emotion], 4),
        "all_scores": {k: round(v, 4) for k, v in emotion_scores.items()},
        "face_detected": face_detected,
    }


# ─── Test ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Testing model loading...")
        try:
            model = _get_model()
            print(f"Input shape:  {model.input_shape}")
            print(f"Output shape: {model.output_shape}")
            print("Model ready!")
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
    else:
        with open(sys.argv[1], "rb") as f:
            result = detect_emotion_from_image(f.read())
        print(f"Emotion: {result['emotion']} ({result['confidence']:.2%})")
        print(f"Face: {result['face_detected']}")
        print(f"Scores: {result['all_scores']}")
