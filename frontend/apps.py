import os
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# =========================
# Config & Constants
# =========================
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Emotion → Music Recommender",
    page_icon="🎧",
    layout="wide"
)

# =========================
# Global Styling
# =========================
APP_CSS = """
<style>
.stApp {
  background: linear-gradient(135deg, #0d0b28 0%, #2c247d 50%, #0e0a3c 100%);
  color: #E9E9EF !important;
  font-family: 'Inter', sans-serif;
}
header, footer {visibility: hidden;}
.title-card {
  background: linear-gradient(90deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
  border-radius: 20px;
  padding: 1.3rem 1.6rem;
  box-shadow: 0 6px 25px rgba(0,0,0,0.3);
  margin-bottom: 1.2rem;
  text-align: center;
}
h1, h2, h3, h4, h5, h6 { color: #FFFFFF !important; }
.stButton>button {
  background: linear-gradient(135deg, #6e3cf7 0%, #7b5cfb 100%);
  color: white;
  border-radius: 12px;
}
.music-card {
  background: rgba(255,255,255,0.05);
  border-radius: 16px;
  padding: 1rem;
}
.song {
  background: rgba(255,255,255,0.07);
  border-radius: 14px;
  padding: 0.75rem;
}
.song-link { color: #a3e8ff !important; }
.divider {
  height: 1px;
  background: rgba(255,255,255,0.3);
  margin: 1rem 0;
}
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)

# =========================
# Header
# =========================
st.markdown("""
<div class='title-card'>
<h1>🎧 Emotion → Music Recommender</h1>
<p>Detect your emotion and get personalized music 🎶</p>
</div>
""", unsafe_allow_html=True)

# =========================
# Session State
# =========================
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = None
if "last_recs" not in st.session_state:
    st.session_state.last_recs = []

# =========================
# Helper Functions
# =========================
def post_text_emotion(text):
    return requests.post(f"{FASTAPI_URL}/predict/text", json={"text": text}).json().get("emotion")

def post_face_emotion_from_bytes(img):
    return requests.post(f"{FASTAPI_URL}/predict/face-image",
                         files={"file": ("img.jpg", img)}).json().get("emotion")

def post_recommendations(emotion, uplift):
    return requests.post(f"{FASTAPI_URL}/recommend",
                         json={"emotion": emotion, "uplift": uplift}).json()

def render_recommendations(recs):
    for r in recs:
        st.markdown(f"""
        <div class='song'>
        🎵 <b>{r.get("name")}</b> - {r.get("artist")} <br>
        <a class='song-link' href='{r.get("link")}' target='_blank'>Open</a>
        </div>
        """, unsafe_allow_html=True)

# =========================
# Tabs
# =========================
tab1, tab2, tab3 = st.tabs(["Face", "Text", "Logic"])

# =========================
# Logic Tab
# =========================
with tab3:
    st.subheader("Emotion Mapping")

    # ✅ FIXED HERE
    col_plot, col_text = st.columns([1, 2])

    with col_plot:
        fig, ax = plt.subplots()
        ax.axhline(0.5)
        ax.axvline(0.5)
        st.pyplot(fig)

    with col_text:
        st.write("Valence-Arousal explanation...")

# =========================
# Face Tab
# =========================
with tab1:
    img = st.file_uploader("Upload image")

    if st.button("Analyze Face"):
        if img:
            emo = post_face_emotion_from_bytes(img.read())
            st.success(f"Emotion: {emo}")
            recs = post_recommendations(emo, False)
            render_recommendations(recs)

# =========================
# Text Tab
# =========================
with tab2:
    txt = st.text_area("Enter text")

    if st.button("Analyze Text"):
        emo = post_text_emotion(txt)
        st.success(f"Emotion: {emo}")
        recs = post_recommendations(emo, False)
        render_recommendations(recs)

# =========================
# Footer
# =========================
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.write("Last Emotion:", st.session_state.last_emotion)
