import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'emotion_model.h5')
INPUT_SIZE = 224

EMOTIONS = ['Angry', 'Disgusted', 'Fearful', 'Happy', 'Neutral', 'Sad', 'Surprised']
EMOJIS   = ['😠', '🤢', '😨', '😄', '😐', '😢', '😮']

model = load_model(MODEL_PATH)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

def predict_from_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30)
    )

    if len(faces) == 0:
        return {'error': 'No face detected', 'faces': []}

    results = []
    for (x, y, w, h) in faces:
        face_roi    = frame[y:y+h, x:x+w]
        face_rgb    = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
        face_resized = cv2.resize(face_rgb, (INPUT_SIZE, INPUT_SIZE))
        face_norm   = face_resized.astype('float32') / 255.0
        face_input  = np.expand_dims(face_norm, axis=0)

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