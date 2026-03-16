import cv2
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'emotion_model.h5')
INPUT_SIZE = 224

EMOTIONS = ['Angry', 'Disgusted', 'Fearful', 'Happy', 'Neutral', 'Sad', 'Surprised']
EMOJIS   = ['😠', '🤢', '😨', '😄', '😐', '😢', '😮']

model = None
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

def load_emotion_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            print("WARNING: emotion_model.h5 not found. Train the model first.")
            return False
        from tensorflow.keras.models import load_model
        model = load_model(MODEL_PATH)
        print("Model loaded successfully.")
    return True

def predict_from_frame(frame):
    if not load_emotion_model():
        import random
        probs = [random.random() for _ in EMOTIONS]
        total = sum(probs)
        probs = [p/total for p in probs]
        dominant_idx = probs.index(max(probs))
        return {
            'faces': [{
                'dominant':      EMOTIONS[dominant_idx],
                'emoji':         EMOJIS[dominant_idx],
                'confidence':    float(probs[dominant_idx]),
                'probabilities': {EMOTIONS[i]: float(probs[i]) for i in range(len(EMOTIONS))},
                'bbox':          {'x': 100, 'y': 100, 'w': 200, 'h': 200},
                'note':          'Demo mode - train model for real predictions'
            }],
            'count': 1
        }

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30,30))

    if len(faces) == 0:
        return {'error': 'No face detected', 'faces': []}

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