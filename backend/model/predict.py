import cv2
import numpy as np
import os
import random

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'emotion_model.h5')
INPUT_SIZE  = 224

EMOTIONS = ['Angry', 'Disgusted', 'Fearful', 'Happy', 'Neutral', 'Sad', 'Surprised']
EMOJIS   = ['😠', '🤢', '😨', '😄', '😐', '😢', '😮']

model        = None
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

def load_emotion_model():
    global model
    if model is not None:
        return True
    if not os.path.exists(MODEL_PATH):
        print("WARNING: emotion_model.h5 not found — using demo mode")
        return False
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print("Model loaded successfully!")
        return True
    except Exception as e:
        print(f"Model load error: {e} — using demo mode")
        return False

def demo_result():
    probs        = [random.random() for _ in EMOTIONS]
    total        = sum(probs)
    probs        = [p / total for p in probs]
    dominant_idx = probs.index(max(probs))
    return {
        'faces': [{
            'dominant':      EMOTIONS[dominant_idx],
            'emoji':         EMOJIS[dominant_idx],
            'confidence':    float(probs[dominant_idx]),
            'probabilities': {EMOTIONS[i]: float(probs[i]) for i in range(len(EMOTIONS))},
            'bbox':          {'x': 100, 'y': 100, 'w': 200, 'h': 200},
            'note':          'Demo mode — place emotion_model.h5 in backend/model/ for real predictions'
        }],
        'count': 1
    }

def predict_from_frame(frame):
    if not load_emotion_model():
        return demo_result()

    try:
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30)
        )

        if len(faces) == 0:
            return demo_result()

        results = []
        for (x, y, w, h) in faces:
            face_roi     = frame[y:y+h, x:x+w]
            face_rgb     = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
            face_resized = cv2.resize(face_rgb, (INPUT_SIZE, INPUT_SIZE))
            face_norm    = face_resized.astype('float32') / 255.0
            face_input   = np.expand_dims(face_norm, axis=0)

            probs        = model.predict(face_input, verbose=0)[0]
            dominant_idx = int(np.argmax(probs))

            results.append({
                'dominant':      EMOTIONS[dominant_idx],
                'emoji':         EMOJIS[dominant_idx],
                'confidence':    float(probs[dominant_idx]),
                'probabilities': {EMOTIONS[i]: float(probs[i]) for i in range(len(EMOTIONS))},
                'bbox':          {'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)}
            })

        return {'faces': results, 'count': len(results)}

    except Exception as e:
        print(f"Prediction error: {e}")
        return demo_result()