import pandas as pd
import numpy as np
import os
import random

# ── Load dataset once globally ──
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'Music_Info.csv')
music_df = pd.read_csv(DATA_PATH)

def track_id_to_spotify_url(track_id):
    return f"https://open.spotify.com/track/{track_id}"

music_df["spotify_url"] = music_df["spotify_id"].apply(track_id_to_spotify_url)

def recommend_songs_by_emotion(emotion: str, n: int = 15, uplift: bool = False):
    """
    Recommend songs based on emotion using valence + energy from Music_Info.csv.
    - uplift=False → Mood-matching (songs that reflect your emotion)
    - uplift=True  → Mood-uplifting (songs that improve your emotion)
    Uses audio features: valence (happiness) and energy (intensity)
    """
    emotion = emotion.lower().strip()

    if not uplift:
        # Mood-matching mode
        if emotion == "sad":
            recs = music_df[(music_df["valence"] < 0.4) & (music_df["energy"] < 0.5)]
        elif emotion == "happy":
            recs = music_df[(music_df["valence"] > 0.6) & (music_df["energy"] > 0.5)]
        elif emotion == "angry":
            recs = music_df[(music_df["valence"] < 0.4) & (music_df["energy"] > 0.7)]
        elif emotion in ["surprise", "surprised"]:
            recs = music_df[(music_df["valence"].between(0.4, 0.7)) & (music_df["energy"] > 0.6)]
        elif emotion in ["fear", "fearful"]:
            recs = music_df[(music_df["valence"] < 0.4) & (music_df["energy"].between(0.3, 0.7))]
        elif emotion == "disgust":
            recs = music_df[(music_df["valence"] < 0.5) & (music_df["energy"].between(0.3, 0.6))]
        else:  # neutral
            recs = music_df[(music_df["valence"].between(0.4, 0.6)) & (music_df["energy"].between(0.4, 0.6))]
    else:
        # Mood-uplifting mode
        if emotion == "sad":
            recs = music_df[(music_df["valence"] > 0.6) & (music_df["energy"].between(0.4, 0.7))]
        elif emotion == "angry":
            recs = music_df[(music_df["valence"] > 0.5) & (music_df["energy"] < 0.5)]
        elif emotion in ["fear", "fearful"]:
            recs = music_df[(music_df["valence"] > 0.6) & (music_df["energy"].between(0.3, 0.6))]
        elif emotion == "disgust":
            recs = music_df[(music_df["valence"] > 0.6) & (music_df["energy"].between(0.4, 0.7))]
        elif emotion == "happy":
            recs = music_df[(music_df["valence"] > 0.6) & (music_df["energy"] > 0.5)]
        elif emotion in ["surprise", "surprised"]:
            recs = music_df[(music_df["valence"].between(0.5, 0.8)) & (music_df["energy"] > 0.6)]
        else:  # neutral
            recs = music_df[(music_df["valence"].between(0.4, 0.6)) & (music_df["energy"].between(0.4, 0.6))]

    # Fallback if no results found
    if recs.empty:
        recs = music_df.sample(n)

    # Randomly sample n songs — different every time
    recs_sampled = recs.sample(min(n, len(recs)))

    results = []
    for _, row in recs_sampled.iterrows():
        results.append({
            "name":       row["name"],
            "artist":     row["artist"],
            "spotify_url": row["spotify_url"],
            "preview_url": row.get("spotify_preview_url", ""),
            "valence":    round(float(row["valence"]), 2),
            "energy":     round(float(row["energy"]), 2),
        })

    return results