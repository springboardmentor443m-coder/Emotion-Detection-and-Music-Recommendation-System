import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from PIL import Image

# Load model
model = load_model("emotion_cnn_model.h5")

# Emotion labels (FER2013)
emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]

st.title("Emotion Detection from Face")
st.write("Upload a face image and the model will predict the emotion.")

# Upload image
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    # Convert to array
    img = np.array(image)

    # Convert to grayscale
    img = np.array(image)

# convert to grayscale only if image has 3 channels
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize to 48x48 (FER2013 size)
    img = cv2.resize(img, (48,48))

    # Normalize
    img = img / 255.0

    # Reshape for model
    img = img.reshape(1,48,48,1)

    # Prediction
    prediction = model.predict(img)
    emotion = emotion_labels[np.argmax(prediction)]

    st.subheader(f"Predicted Emotion: {emotion}")