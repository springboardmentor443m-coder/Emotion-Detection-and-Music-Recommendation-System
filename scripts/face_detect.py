from pathlib import Path

import cv2
import numpy as np
from tensorflow.keras.models import load_model

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "backend" / "best_model.keras"

# Load trained model
model = load_model(MODEL_PATH)

# Emotion labels (6 classes)
emotion_labels = ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:

        # Draw rectangle
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        # Crop face
        face = gray[y:y+h, x:x+w]

        # Resize to model input
        face = cv2.resize(face, (48, 48))

        # Normalize
        face = face / 255.0

        # Reshape
        face = np.reshape(face, (1, 48, 48, 1))

        # Predict
        preds = model.predict(face, verbose=0)
        label = emotion_labels[np.argmax(preds)]
        confidence = np.max(preds) * 100

        text = f"{label} ({confidence:.1f}%)"

        # Put text
        cv2.putText(frame, text, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    # Show frame
    cv2.imshow("Emotion Detection (Press Q to exit)", frame)

    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam
cap.release()
cv2.destroyAllWindows()
