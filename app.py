import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import streamlit.components.v1 as components

# Load model
model = tf.keras.models.load_model("mobilenetv2.keras")

# Emotion labels
emotions = ['Angry', 'Happy', 'Sad', 'Surprise', 'Neutral']

# 🎵 Music Recommendation
def recommend_music(emotion):
    music = {
        "Happy": [
            "09ZQ5TmUG8TSL56n0knqrj",
            "3n3Ppam7vgaVa1iaRUc9Lp",
            "1VdZ0vKfR5jneCmWIUAMxK",
            "7qiZfU4dY1lWllzX7mPBI3",
            "0nrRP2bk19rLc0orkWPQk2",
            "6habFhsOp2NvshLv26DqMb"
        ],
        "Sad": [
            "06UFBBDISttj1ZJAtX4xJj",
            "4uLU6hMCjMI75M1A2tKUQC",
            "1HNkqx9Ahdgi1Ixy2xkKkL",
            "3AJwUDP919kvQ9QcozQPxg",
            "0QZ5yyl6B6utIWkxeBDxQN"
        ],
        "Angry": [
            "7MXVkk9YMctZqd1Srtv4MB",
            "6habFhsOp2NvshLv26DqMb",
            "5CQ30WqJwcep0pYcV4AMNc",
            "7yq4Qj7cqayVTp3FF9CWbm",
            "6Vh03bkEfXqL4h0W6jJ9m3"
        ],
        "Surprise": [
            "7ouMYWpwJ422jRcDASZB7P",
            "0VjIjW4GlUZAMYd2vXMi3b",
            "3KkXRkHbMCARz0aVfEt68P",
            "5Z01UMMf7V1o0MzF86s6WJ"
        ],
        "Neutral": [
            "3n3Ppam7vgaVa1iaRUc9Lp",
            "2Fxmhks0bxGSBdJ92vM42m",
            "4iV5W9uYEdYUVa79Axb7Rh",
            "1zB4vmk8tFRmM9UULNzbLB",
            "6DCZcSspjsKoFjzjrWoCdn"
        ]
    }

    return music.get(emotion, [])

# 🎨 UI STYLE
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.title {
    font-size: 70px;
    color: white;
    text-align: center;
    font-weight: bold;
    text-shadow: 0px 0px 20px rgba(255,255,255,0.9),
                 0px 0px 40px rgba(29,185,84,0.8);
}
.subtitle {
    text-align: center;
    font-size: 22px;
    color: #cccccc;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎧 Emotion Detection + Music Recommendation</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze your mood and get songs 🎶</div>', unsafe_allow_html=True)

# Prediction function
def predict_emotion(image):
    image = image.resize((128, 128))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    emotion_index = np.argmax(prediction)
    emotion = emotions[emotion_index]
    confidence = np.max(prediction) * 100

    return emotion, confidence

# 🎵 Display music
def show_music(emotion):
    st.markdown("## 🎵 Recommended Songs")
    songs = recommend_music(emotion)
    for song in songs:
        components.iframe(
            f"https://open.spotify.com/embed/track/{song}",
            height=80
        )

# Input selection
option = st.selectbox("Choose Input Type", ["Image", "Webcam", "Video", "Text"])

# 🖼 IMAGE
if option == "Image":
    file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if file:
        image = Image.open(file).convert("RGB")
        st.image(image, use_container_width=True)

        emotion, confidence = predict_emotion(image)

        st.success(f"Emotion: {emotion}")
        st.info(f"Confidence: {confidence:.2f}%")

        show_music(emotion)

# 📸 WEBCAM
elif option == "Webcam":
    img = st.camera_input("Take a picture")

    if img:
        image = Image.open(img).convert("RGB")
        st.image(image, use_container_width=True)

        emotion, confidence = predict_emotion(image)

        st.success(f"Emotion: {emotion}")
        st.info(f"Confidence: {confidence:.2f}%")

        show_music(emotion)

# 🎥 VIDEO
elif option == "Video":
    video = st.file_uploader("Upload Video", type=["mp4", "avi"])

    if video:
        st.video(video)

        with open("temp.mp4", "wb") as f:
            f.write(video.read())

        cap = cv2.VideoCapture("temp.mp4")
        ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)

            emotion, confidence = predict_emotion(image)

            st.success(f"Emotion (First Frame): {emotion}")
            st.info(f"Confidence: {confidence:.2f}%")

            show_music(emotion)

        cap.release()

# ✍️ TEXT
elif option == "Text":
    text = st.text_area("Enter your text")

    if text:
        text = text.lower()

        if "happy" in text:
            emotion = "Happy"
        elif "sad" in text:
            emotion = "Sad"
        elif "angry" in text:
            emotion = "Angry"
        elif "surprise" in text:
            emotion = "Surprise"
        else:
            emotion = "Neutral"

        st.success(f"Detected Emotion: {emotion}")

        show_music(emotion)