import os
import sqlite3
from pathlib import Path

import cv2
import numpy as np
import spotipy
from database import clear_mood_history
from database import fetch_mood_history
from database import init_db
from database import save_mood_history
from flask import Flask, jsonify, request
from flask_cors import CORS
from music_recommender import recommend_music
from spotipy.oauth2 import SpotifyClientCredentials
from text_emotion_detector import predict_text_emotion as predict_text_from_bundle
from text_emotion_detector import TEXT_DATASET_PATH
from text_emotion_detector import TEXT_NOTEBOOK_PATH
from text_emotion_detector import train_text_model
from tensorflow.keras.models import load_model

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "best_model.keras"
DB_PATH = BASE_DIR / "music.db"
FACE_CASCADE_PATH = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"

app = Flask(__name__)
CORS(app)

init_db()
model = load_model(MODEL_PATH)
emotion_labels = ["Angry", "Fear", "Happy", "Neutral", "Sad", "Surprise"]
face_cascade = cv2.CascadeClassifier(str(FACE_CASCADE_PATH))


def create_spotify_client():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        return None

    return spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )
    )


sp = create_spotify_client()
text_model_bundle = train_text_model()


def predict_emotion(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) > 0:
        # Use the largest detected face to match the standalone detector flow.
        x, y, w, h = max(faces, key=lambda item: item[2] * item[3])
        gray = gray[y:y + h, x:x + w]

    face = cv2.resize(gray, (48, 48))
    face = face / 255.0
    face = np.reshape(face, (1, 48, 48, 1))

    prediction = model.predict(face, verbose=0)
    predicted_index = int(np.argmax(prediction))

    if predicted_index >= len(emotion_labels):
        raise ValueError(
            f"Model predicted class index {predicted_index}, but only {len(emotion_labels)} labels are configured."
        )

    return emotion_labels[predicted_index]


def predict_text_emotion(text):
    return predict_text_from_bundle(text_model_bundle, text)


def get_dataset_songs(emotion):
    try:
        _, songs = recommend_music(emotion)
    except Exception:
        return []

    return songs


def get_local_songs(emotion):
    mood_aliases = {
        "Happy": ["happy", "pop", "dance"],
        "Sad": ["sad", "acoustic"],
        "Angry": ["angry", "rock"],
        "Fear": ["fear", "calm"],
        "Surprise": ["surprise", "dance", "pop"],
        "Neutral": ["neutral", "calm", "lofi"],
    }

    search_terms = mood_aliases.get(emotion, [emotion.lower()])

    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            placeholders = ",".join("?" for _ in search_terms)
            query = f"""
                SELECT title, artist
                FROM music
                WHERE lower(mood) IN ({placeholders}) OR lower(genre) IN ({placeholders})
                LIMIT 5
            """
            params = [term.lower() for term in search_terms] * 2
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()

            if rows:
                return [
                    {
                        "title": title,
                        "artist": artist,
                        "track_id": "",
                        "image": "",
                        "spotify_search_url": "",
                    }
                    for title, artist in rows
                ]
        except Exception:
            pass

    fallback_catalog = {
        "Happy": [
            {"title": "Shape of You", "artist": "Ed Sheeran", "track_id": "", "image": ""},
            {"title": "Blinding Lights", "artist": "The Weeknd", "track_id": "", "image": ""},
        ],
        "Sad": [
            {"title": "Someone Like You", "artist": "Adele", "track_id": "", "image": ""},
            {"title": "Let Her Go", "artist": "Passenger", "track_id": "", "image": ""},
        ],
        "Angry": [
            {"title": "Believer", "artist": "Imagine Dragons", "track_id": "", "image": ""},
            {"title": "Thunder", "artist": "Imagine Dragons", "track_id": "", "image": ""},
        ],
        "Fear": [
            {"title": "Weightless", "artist": "Ambient", "track_id": "", "image": ""},
        ],
        "Neutral": [
            {"title": "Weightless", "artist": "Ambient", "track_id": "", "image": ""},
            {"title": "Perfect", "artist": "Ed Sheeran", "track_id": "", "image": ""},
        ],
        "Surprise": [
            {"title": "Blinding Lights", "artist": "The Weeknd", "track_id": "", "image": ""},
        ],
    }

    normalized = []
    for song in fallback_catalog.get(emotion, fallback_catalog["Neutral"]):
        entry = dict(song)
        entry["spotify_search_url"] = ""
        normalized.append(entry)

    return normalized


def merge_song_lists(*song_lists):
    merged = []
    seen = set()

    for song_list in song_lists:
        for song in song_list:
            dedupe_key = (
                str(song.get("title", "")).strip().lower(),
                str(song.get("artist", "")).strip().lower(),
            )

            if dedupe_key in seen:
                continue

            seen.add(dedupe_key)
            song.setdefault("track_id", "")
            song.setdefault("image", "")
            song.setdefault("spotify_search_url", "")
            merged.append(song)

    return merged[:6]


def recommend_songs(emotion):
    emotion_to_query = {
        "Happy": "happy upbeat",
        "Sad": "sad songs",
        "Angry": "rock intense",
        "Neutral": "lofi chill",
        "Surprise": "party",
        "Fear": "calm relaxing",
    }

    dataset_songs = get_dataset_songs(emotion)

    if sp is None:
        return merge_song_lists(dataset_songs, get_local_songs(emotion))

    query = emotion_to_query.get(emotion, "trending songs")
    results = sp.search(q=query, limit=12, type="track")

    songs = []
    spotify_items = results["tracks"]["items"]

    for track in spotify_items[:5]:
        image_url = ""
        if track["album"]["images"]:
            image_url = track["album"]["images"][0]["url"]

        songs.append(
            {
                "title": track["name"],
                "artist": track["artists"][0]["name"],
                "track_id": track["id"],
                "image": image_url,
                "spotify_search_url": track["external_urls"].get("spotify", ""),
            }
        )

    return merge_song_lists(songs, dataset_songs, get_local_songs(emotion))


@app.route("/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "ok",
            "spotify_configured": sp is not None,
            "model_path": str(MODEL_PATH),
            "text_model_notebook": str(TEXT_NOTEBOOK_PATH),
            "text_model_dataset": str(TEXT_DATASET_PATH),
            "text_model_loaded": True,
            "history_enabled": True,
        }
    )


@app.route("/history", methods=["GET"])
def get_history():
    return jsonify({"history": fetch_mood_history()})


@app.route("/history", methods=["DELETE"])
def delete_history():
    clear_mood_history()
    return jsonify({"status": "cleared"})


@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("image")
    if file is None:
        return jsonify({"error": "Missing image upload."}), 400

    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image data."}), 400

    emotion = predict_emotion(img)

    try:
        songs = recommend_songs(emotion)
    except Exception as error:
        return jsonify(
            {
                "error": "Could not fetch songs from Spotify.",
                "details": str(error),
                "emotion": emotion,
            }
        ), 502

    save_mood_history("image", emotion)

    return jsonify(
        {
            "emotion": emotion,
            "songs": songs,
        }
    )


@app.route("/predict-text", methods=["POST"])
def predict_text():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")

    if not text or not text.strip():
        return jsonify({"error": "Missing text input."}), 400

    try:
        emotion = predict_text_emotion(text)
        songs = recommend_songs(emotion)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        return jsonify(
            {
                "error": "Could not process text mood prediction.",
                "details": str(error),
            }
        ), 500

    save_mood_history("text", emotion, text.strip())

    return jsonify(
        {
            "emotion": emotion,
            "songs": songs,
            "source": "text_model",
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
