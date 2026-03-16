import streamlit as st
import requests
import streamlit.components.v1 as components

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

h1 {
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# PAGE CONFIG
st.set_page_config(
    page_title="AI MoodMate",
    page_icon="🎵",
    layout="centered"
)

# HEADER
st.markdown(
    """
    <h1 style='text-align: center;'>🎵 AI MoodMate</h1>
    <p style='text-align: center; font-size:18px;'>
    Detect your emotion and get music that matches your mood
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# INPUT METHOD
input_method = st.radio(
    "Choose input method",
    ["Upload Image", "Use Webcam"],
    horizontal=True
)

image = None

# LAYOUT
left, right = st.columns([1,1])

# IMAGE UPLOAD
if input_method == "Upload Image":
    with left:

        uploaded_file = st.file_uploader(
            "Upload your face image",
            type=["jpg","png","jpeg"]
        )

        if uploaded_file:
            image = uploaded_file.getvalue()

            st.image(uploaded_file, caption="Uploaded Image")

# WEBCAM
if input_method == "Use Webcam":
    with left:

        captured_image = st.camera_input("Take a photo")

        if captured_image:
            image = captured_image.getvalue()

            st.image(captured_image)

# DETECT BUTTON
if image:

    with right:

        if st.button("🎯 Detect Emotion & Recommend Music", use_container_width=True):

            with st.spinner("Analyzing emotion..."):

                files = {"image": image}

                response = requests.post(
                    "http://127.0.0.1:5000/recommend",
                    files=files
                )

                data = response.json()

            st.success(f"Detected Emotion: **{data['emotion'].capitalize()}**")

            st.markdown("### 🎧 Recommended Songs")

            for song in data["songs"]:

                st.subheader(f"{song['name']} — {song['artist']}")

                embed_url = f"https://open.spotify.com/embed/track/{song['spotify_id']}?utm_source=generator&theme=0"
                components.iframe(embed_url, height=80)