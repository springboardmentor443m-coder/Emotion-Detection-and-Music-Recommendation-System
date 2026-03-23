"""
Streamlit Frontend for Emotion-Based Music Recommender

Provides two input modes:
  1. Text — Describe your feelings
  2. Image — Upload a facial photo or use webcam

Displays detected emotion and recommended songs.
"""

import streamlit as st
import requests
import json
from io import BytesIO

# ─── Configuration ────────────────────────────────────────────────────────────

API_BASE_URL = "http://localhost:8000"

EMOTION_EMOJIS = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "surprise": "😲",
    "neutral": "😐",
}

EMOTION_COLORS = {
    "happy": "#FFD700",
    "sad": "#4169E1",
    "angry": "#DC143C",
    "surprise": "#FF6347",
    "neutral": "#708090",
}

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="🎵 Emotion Music Recommender",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }

    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        text-align: center;
        color: #a0a0c0;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }

    /* Emotion card */
    .emotion-card {
        background: linear-gradient(145deg, #1e1e3f, #2a2a5e);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin: 1rem 0;
    }

    .emotion-emoji {
        font-size: 4rem;
        margin-bottom: 0.5rem;
    }

    .emotion-label {
        font-size: 1.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }

    .confidence-text {
        color: #a0a0c0;
        font-size: 1rem;
    }

    /* Song card */
    .song-card {
        background: linear-gradient(145deg, #1a1a3e, #252550);
        border-radius: 16px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .song-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }

    .song-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #e0e0ff;
        margin-bottom: 0.3rem;
    }

    .song-artist {
        color: #9090c0;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }

    .song-meta {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .song-badge {
        background: rgba(102, 126, 234, 0.2);
        color: #8899ee;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        display: inline-block;
    }

    .spotify-link {
        display: inline-block;
        background: #1DB954;
        color: white !important;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        text-decoration: none;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.5rem;
        transition: background 0.2s;
    }

    .spotify-link:hover {
        background: #1ed760;
    }

    /* Score bars */
    .score-bar-container {
        margin: 0.3rem 0;
    }

    .score-bar-label {
        display: flex;
        justify-content: space-between;
        color: #b0b0d0;
        font-size: 0.85rem;
        margin-bottom: 0.15rem;
    }

    .score-bar {
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        overflow: hidden;
    }

    .score-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a3e, #0f0c29);
    }

    /* Divider */
    .section-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.4), transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ─── Helper Functions ─────────────────────────────────────────────────────────

def check_api_health():
    """Check if the backend API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def detect_text_emotion(text: str, num_songs: int = 5) -> dict:
    """Call the text emotion detection API."""
    response = requests.post(
        f"{API_BASE_URL}/api/detect-text",
        json={"text": text, "num_songs": num_songs},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def detect_image_emotion(image_bytes: bytes, num_songs: int = 5) -> dict:
    """Call the image emotion detection API."""
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    params = {"num_songs": num_songs}
    response = requests.post(
        f"{API_BASE_URL}/api/detect-image",
        files=files,
        params=params,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def render_emotion_card(emotion: str, confidence: float, all_scores: dict):
    """Render the detected emotion display card."""
    emoji = EMOTION_EMOJIS.get(emotion, "🎭")
    color = EMOTION_COLORS.get(emotion, "#667eea")

    st.markdown(f"""
    <div class="emotion-card">
        <div class="emotion-emoji">{emoji}</div>
        <div class="emotion-label" style="color: {color};">{emotion}</div>
        <div class="confidence-text">Confidence: {confidence:.1%}</div>
    </div>
    """, unsafe_allow_html=True)

    # Score breakdown
    st.markdown("#### 📊 Emotion Scores")
    for emo, score in sorted(all_scores.items(), key=lambda x: x[1], reverse=True):
        emo_color = EMOTION_COLORS.get(emo, "#667eea")
        emo_emoji = EMOTION_EMOJIS.get(emo, "")
        width = max(score * 100, 2)

        st.markdown(f"""
        <div class="score-bar-container">
            <div class="score-bar-label">
                <span>{emo_emoji} {emo.capitalize()}</span>
                <span>{score:.1%}</span>
            </div>
            <div class="score-bar">
                <div class="score-bar-fill" style="width: {width}%; background: {emo_color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_song_cards(recommendation: dict):
    """Render song recommendation cards."""
    st.markdown(f"### 🎵 {recommendation['description']}")
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    songs = recommendation.get("songs", [])
    if not songs:
        st.warning("No songs found for this mood. Try a different input!")
        return

    for song in songs:
        spotify_link = song.get("spotify_url", "")
        link_html = f'<a href="{spotify_link}" target="_blank" class="spotify-link">▶ Play on Spotify</a>' if spotify_link else ""

        st.markdown(f"""
        <div class="song-card">
            <div class="song-title">🎶 {song['title']}</div>
            <div class="song-artist">{song['artist']}</div>
            <div class="song-meta">
                <span class="song-badge">🎸 {song['genre']}</span>
                <span class="song-badge">💖 Valence: {song['valence']}</span>
                <span class="song-badge">⚡ Energy: {song['energy']}</span>
                <span class="song-badge">🥁 {song['tempo']} BPM</span>
            </div>
            {link_html}
        </div>
        """, unsafe_allow_html=True)


# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚙️ Settings")

    num_songs = st.slider("Number of songs", min_value=3, max_value=10, value=5)

    st.markdown("---")

    st.markdown("## 📖 How it works")
    st.markdown("""
    1. **Choose input mode** — Text or Image
    2. **Enter your input** — Describe feelings or upload a photo
    3. **AI detects emotion** — Using NLP or CNN models
    4. **Get recommendations** — Songs matching your mood!
    """)

    st.markdown("---")

    st.markdown("## 🧠 Models Used")
    st.markdown("""
    - **Text**: DistilRoBERTa (HuggingFace)
    - **Image**: MobileNetV2 (Transfer Learning)
    - **Dataset**: FER-2013 (facial emotions)
    """)

    st.markdown("---")

    # API Status
    api_healthy = check_api_health()
    if api_healthy:
        st.success("🟢 Backend API is running")
    else:
        st.error("🔴 Backend API is not running")
        st.info("Start it with:\n```\nuvicorn backend.main:app --port 8000\n```")


# ─── Main Content ─────────────────────────────────────────────────────────────

st.markdown('<h1 class="main-header">🎵 Emotion Music Recommender</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Detect your mood from text or facial expression, get personalized song recommendations</p>', unsafe_allow_html=True)

# Input mode tabs
tab_text, tab_image = st.tabs(["📝 Text Input", "📷 Image Input"])

# ─── Text Tab ─────────────────────────────────────────────────────────────────

with tab_text:
    st.markdown("### How are you feeling?")
    st.markdown("*Describe your current mood, thoughts, or feelings...*")

    text_input = st.text_area(
        "Enter your text",
        height=150,
        placeholder="e.g., I'm feeling really happy today! The sun is shining and everything feels great.",
        label_visibility="collapsed",
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        detect_text_btn = st.button(
            "🔍 Detect Emotion & Get Songs",
            key="text_btn",
            use_container_width=True,
            type="primary",
        )

    if detect_text_btn:
        if not text_input or not text_input.strip():
            st.warning("Please enter some text first!")
        elif not check_api_health():
            st.error("Backend API is not running. Please start it first.")
        else:
            with st.spinner("🧠 Analyzing your emotions..."):
                try:
                    result = detect_text_emotion(text_input, num_songs)

                    col_emo, col_songs = st.columns([1, 2])

                    with col_emo:
                        render_emotion_card(
                            result["emotion"],
                            result["confidence"],
                            result["all_scores"],
                        )

                    with col_songs:
                        render_song_cards(result["recommendation"])

                except requests.exceptions.RequestException as e:
                    st.error(f"API Error: {str(e)}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# ─── Image Tab ────────────────────────────────────────────────────────────────

with tab_image:
    st.markdown("### Upload a facial photo")
    st.markdown("*Upload a clear photo of your face for emotion detection*")

    upload_col, camera_col = st.columns(2)

    with upload_col:
        st.markdown("#### 📁 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png", "bmp"],
            label_visibility="collapsed",
        )

    with camera_col:
        st.markdown("#### 📸 Take a Photo")
        camera_photo = st.camera_input(
            "Take a photo",
            label_visibility="collapsed",
        )

    # Use whichever input is available
    image_bytes = None
    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
        st.image(uploaded_file, caption="Uploaded Image", width=300)
    elif camera_photo is not None:
        image_bytes = camera_photo.getvalue()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        detect_image_btn = st.button(
            "🔍 Detect Emotion & Get Songs",
            key="image_btn",
            use_container_width=True,
            type="primary",
        )

    if detect_image_btn:
        if image_bytes is None:
            st.warning("Please upload an image or take a photo first!")
        elif not check_api_health():
            st.error("Backend API is not running. Please start it first.")
        else:
            with st.spinner("🧠 Analyzing facial expression..."):
                try:
                    result = detect_image_emotion(image_bytes, num_songs)

                    # Face detection status
                    if result.get("face_detected"):
                        st.success("✅ Face detected in the image")
                    else:
                        st.warning("⚠️ No face detected — using full image for analysis")

                    col_emo, col_songs = st.columns([1, 2])

                    with col_emo:
                        render_emotion_card(
                            result["emotion"],
                            result["confidence"],
                            result["all_scores"],
                        )

                    with col_songs:
                        render_song_cards(result["recommendation"])

                except requests.exceptions.RequestException as e:
                    st.error(f"API Error: {str(e)}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# ─── Footer ──────────────────────────────────────────────────────────────────

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align: center; color: #606090; font-size: 0.85rem;">'
    'Built with ❤️ using FastAPI, Streamlit, MobileNetV2 & HuggingFace Transformers'
    '</p>',
    unsafe_allow_html=True,
)
