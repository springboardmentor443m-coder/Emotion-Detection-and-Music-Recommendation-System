"""
Music Recommendation Engine

Maps detected emotions to song recommendations based on
valence and energy metrics from the song dataset CSV.
"""

import os
import random
import pandas as pd

# ─── Configuration ────────────────────────────────────────────────────────────

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "song_dataset.csv")

# Emotion-to-audio-feature mapping
# Each emotion maps to target valence/energy ranges
EMOTION_PROFILES = {
    "happy": {
        "valence_min": 0.70,
        "valence_max": 1.00,
        "energy_min": 0.55,
        "energy_max": 1.00,
        "description": "Upbeat and energetic music to match your joyful mood",
    },
    "sad": {
        "valence_min": 0.00,
        "valence_max": 0.30,
        "energy_min": 0.00,
        "energy_max": 0.55,
        "description": "Mellow and soothing music for contemplative moments",
    },
    "angry": {
        "valence_min": 0.00,
        "valence_max": 0.40,
        "energy_min": 0.75,
        "energy_max": 1.00,
        "description": "Intense and powerful music to channel your energy",
    },
    "surprise": {
        "valence_min": 0.35,
        "valence_max": 0.65,
        "energy_min": 0.55,
        "energy_max": 1.00,
        "description": "Dynamic and eclectic songs to match your excitement",
    },
    "neutral": {
        "valence_min": 0.35,
        "valence_max": 0.60,
        "energy_min": 0.05,
        "energy_max": 0.65,
        "description": "Calm and balanced playlist for a relaxed state of mind",
    },
}

# ─── Data Loading ─────────────────────────────────────────────────────────────

_songs_df = None


def _get_songs_df() -> pd.DataFrame:
    """Lazy-load the song dataset."""
    global _songs_df
    if _songs_df is None:
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Song dataset not found at: {DATA_PATH}")
        _songs_df = pd.read_csv(DATA_PATH)
        print(f"[INFO] Loaded {len(_songs_df)} songs from dataset.")
    return _songs_df


# ─── Recommendation Logic ────────────────────────────────────────────────────

def recommend_songs(emotion: str, num_songs: int = 5) -> dict:
    """
    Recommend songs based on detected emotion.

    Strategy:
    1. First, try to match by mood_tag (exact match)
    2. Then, filter by valence/energy ranges
    3. If not enough, relax criteria and pick from closest matches

    Args:
        emotion: Detected emotion (happy, sad, angry, surprise, neutral)
        num_songs: Number of songs to recommend

    Returns:
        dict with keys:
            - emotion: The emotion used for matching
            - description: Description of the mood
            - songs: List of recommended song dicts
    """
    df = _get_songs_df()

    if emotion not in EMOTION_PROFILES:
        emotion = "neutral"

    profile = EMOTION_PROFILES[emotion]

    # Strategy 1: Exact mood_tag match
    mood_matches = df[df["mood_tag"] == emotion].copy()

    if len(mood_matches) >= num_songs:
        # Shuffle and pick
        selected = mood_matches.sample(n=num_songs, random_state=random.randint(0, 9999))
    else:
        # Strategy 2: Valence/energy range matching
        range_matches = df[
            (df["valence"] >= profile["valence_min"]) &
            (df["valence"] <= profile["valence_max"]) &
            (df["energy"] >= profile["energy_min"]) &
            (df["energy"] <= profile["energy_max"])
        ].copy()

        combined = pd.concat([mood_matches, range_matches]).drop_duplicates()

        if len(combined) >= num_songs:
            selected = combined.sample(n=num_songs, random_state=random.randint(0, 9999))
        else:
            # Strategy 3: Score all songs by distance to target profile
            target_valence = (profile["valence_min"] + profile["valence_max"]) / 2
            target_energy = (profile["energy_min"] + profile["energy_max"]) / 2

            df_scored = df.copy()
            df_scored["score"] = (
                abs(df_scored["valence"] - target_valence) +
                abs(df_scored["energy"] - target_energy)
            )
            df_scored = df_scored.sort_values("score")
            selected = df_scored.head(num_songs)

    # Convert to list of dicts
    songs = []
    for _, row in selected.iterrows():
        songs.append({
            "title": row["title"],
            "artist": row["artist"],
            "genre": row["genre"],
            "valence": round(float(row["valence"]), 2),
            "energy": round(float(row["energy"]), 2),
            "tempo": int(row["tempo"]),
            "mood_tag": row["mood_tag"],
            "spotify_url": row.get("spotify_url", ""),
        })

    return {
        "emotion": emotion,
        "description": profile["description"],
        "songs": songs,
        "total_matches": len(mood_matches),
    }


def get_all_songs() -> list:
    """Return all songs in the dataset."""
    df = _get_songs_df()
    return df.to_dict(orient="records")


def get_emotion_profiles() -> dict:
    """Return the emotion-to-audio-feature profiles."""
    return EMOTION_PROFILES


# ─── Test ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  Music Recommendation Engine Test")
    print("=" * 60)

    for emotion in EMOTION_PROFILES:
        result = recommend_songs(emotion, num_songs=3)
        print(f"\n🎵 Mood: {emotion.upper()}")
        print(f"   {result['description']}")
        for song in result["songs"]:
            print(f"   - {song['title']} by {song['artist']} ({song['genre']})")
            print(f"     Valence: {song['valence']} | Energy: {song['energy']}")
