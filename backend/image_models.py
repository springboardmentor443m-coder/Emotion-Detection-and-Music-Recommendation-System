"""
MoodMate - Image Emotion Detection Models
Uses:
  - Custom CNN (emotion_model.keras) - trained on FER-2013, 7 emotions
  - DeepFace (fallback) - pre-trained Facebook AI library
  - OpenCV Haar Cascade - for face detection
"""

import cv2
import numpy as np
import os
from collections import Counter

# ── Try loading tf_keras (your project uses tf_keras) ──
try:
    import tf_keras as keras
    print("✅ tf_keras loaded")
except ImportError:
    try:
        from tensorflow import keras
        print("✅ tensorflow.keras loaded")
    except ImportError:
        keras = None
        print("⚠️  keras not available")

# ── Try loading DeepFace as fallback ──
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
    print("✅ DeepFace loaded")
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("⚠️  DeepFace not installed")

# ── Model path — your trained CNN ──
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    '..', 'models', 'emotion_model.keras'
)

# ── 7 emotion labels matching FER-2013 training order ──
EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# ── Load model once when backend starts ──
model = None
if keras is not None and os.path.exists(MODEL_PATH):
    try:
        model = keras.models.load_model(MODEL_PATH)
        print(f"✅ Custom CNN loaded: {MODEL_PATH}")
    except Exception as e:
        print(f"⚠️  Could not load CNN model: {e}")
        model = None
else:
    if not os.path.exists(MODEL_PATH):
        print(f"⚠️  Model file not found at: {MODEL_PATH}")

# ── OpenCV face detector ──
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)


def predict_emotion_image(img_path: str) -> str:
    """
    Detect emotion from an uploaded image file.

    Steps:
    1. Read image using OpenCV
    2. Detect face using Haar Cascade
    3. Crop and resize face to 48x48
    4. Normalize pixel values to 0-1
    5. Predict using CNN model
    6. Return emotion with highest probability

    Falls back to DeepFace if CNN model not available.
    Falls back to brightness analysis if neither available.
    """

    # ── Try CNN model first ──
    if model is not None:
        try:
            image = cv2.imread(img_path)
            if image is None:
                raise ValueError("Could not read image")

            # Convert to grayscale for CNN (trained on grayscale)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Detect face in image
            faces = detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            if len(faces) > 0:
                # Take the first detected face
                (x, y, w, h) = faces[0]

                # Crop face from image
                face_crop = gray[y:y+h, x:x+w]

                # Resize to 48x48 (CNN input size)
                face_resized = cv2.resize(face_crop, (48, 48))

                # Reshape and normalize: (1, 48, 48, 1) values 0-1
                face_input = face_resized.reshape(1, 48, 48, 1) / 255.0

                # Predict emotion
                prediction = model.predict(face_input, verbose=0)

                # Get emotion with highest probability
                emotion_index = np.argmax(prediction)
                emotion       = EMOTION_LABELS[emotion_index]
                confidence    = float(np.max(prediction))

                print(f"✅ CNN detected: {emotion} ({confidence:.2f})")
                return emotion

        except Exception as e:
            print(f"⚠️  CNN prediction failed: {e} — trying DeepFace")

    # ── Fallback: DeepFace ──
    if DEEPFACE_AVAILABLE:
        try:
            result   = DeepFace.analyze(
                img_path=img_path,
                actions=["emotion"],
                enforce_detection=False,
                silent=True
            )
            if isinstance(result, list):
                result = result[0]
            emotion = result["dominant_emotion"].lower()
            print(f"✅ DeepFace detected: {emotion}")
            return emotion
        except Exception as e:
            print(f"⚠️  DeepFace failed: {e}")

    # ── Last fallback: brightness analysis ──
    print("⚠️  Using brightness fallback")
    return _brightness_fallback(img_path)


def predict_emotion_image_with_confidence(img_path: str) -> dict:
    """
    Same as predict_emotion_image but also returns confidence score.
    Returns: {"emotion": "happy", "confidence": 0.72, "method": "cnn"}
    """

    if model is not None:
        try:
            image = cv2.imread(img_path)
            if image is None:
                raise ValueError("Could not read image")

            gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                face_crop    = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face_crop, (48, 48))
                face_input   = face_resized.reshape(1, 48, 48, 1) / 255.0
                prediction   = model.predict(face_input, verbose=0)

                emotion_index = np.argmax(prediction)
                return {
                    "emotion":    EMOTION_LABELS[emotion_index],
                    "confidence": round(float(np.max(prediction)), 2),
                    "method":     "cnn"
                }
        except Exception as e:
            print(f"⚠️  CNN failed: {e}")

    if DEEPFACE_AVAILABLE:
        try:
            result = DeepFace.analyze(
                img_path=img_path,
                actions=["emotion"],
                enforce_detection=False,
                silent=True
            )
            if isinstance(result, list):
                result = result[0]
            emo   = result["dominant_emotion"].lower()
            score = result["emotion"].get(emo, 50) / 100.0
            return {
                "emotion":    emo,
                "confidence": round(score, 2),
                "method":     "deepface"
            }
        except Exception as e:
            print(f"⚠️  DeepFace failed: {e}")

    emo = _brightness_fallback(img_path)
    return {"emotion": emo, "confidence": 0.55, "method": "fallback"}


def predict_emotion_webcam() -> str:
    """
    Detect emotion from live webcam by capturing 20 frames
    and returning the majority emotion detected.

    Used by the backend webcam endpoint.
    NOTE: Only works when FastAPI runs on the same machine as the webcam.
    """

    cap              = cv2.VideoCapture(0)
    emotions_detected = []
    frame_count      = 0
    total_frames     = 20

    while frame_count < total_frames:
        ret, frame = cap.read()
        if not ret:
            break

        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            if model is not None:
                try:
                    face_crop    = gray[y:y+h, x:x+w]
                    face_resized = cv2.resize(face_crop, (48, 48))
                    face_input   = face_resized.reshape(1, 48, 48, 1) / 255.0
                    prediction   = model.predict(face_input, verbose=0)
                    emotion      = EMOTION_LABELS[np.argmax(prediction)]
                    emotions_detected.append(emotion)
                except Exception:
                    pass

        frame_count += 1

    cap.release()

    if emotions_detected:
        majority_emotion = Counter(emotions_detected).most_common(1)[0][0]
        return majority_emotion

    return "neutral"


def _brightness_fallback(img_path: str) -> str:
    """
    Very basic fallback when no model is available.
    Uses image brightness and color to guess emotion.
    """
    try:
        image      = cv2.imread(img_path)
        if image is None:
            return "neutral"
        gray       = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        contrast   = np.std(gray)

        if   brightness > 155 and contrast > 40:  return "happy"
        elif brightness > 130:                     return "neutral"
        elif brightness > 100 and contrast > 50:  return "surprise"
        elif brightness > 80:                      return "sad"
        else:                                      return "neutral"
    except Exception:
        return "neutral"
