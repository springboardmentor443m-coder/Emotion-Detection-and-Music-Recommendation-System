import urllib.parse
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
SONG_DATA_PATH = PROJECT_ROOT / "data" / "music" / "data.csv"

# MoodMate uses a simple rule-based recommender:
# 1. detect the user's emotion
# 2. map that emotion to a small audio profile
# 3. filter the dataset to songs that fit that profile
# 4. sample a few songs to keep the output varied
EMOTION_AUDIO_RULES = {
    "Happy": {
        "valence": (0.60, 1.00),
        "energy": (0.50, 1.00),
        "genres": ["pop", "dance", "party", "upbeat", "feel good"],
    },
    "Sad": {
        "valence": (0.00, 0.40),
        "energy": (0.00, 0.50),
        "genres": ["acoustic", "soft", "piano", "melancholy", "slow"],
    },
    "Angry": {
        "valence": (0.00, 0.40),
        "energy": (0.70, 1.00),
        "genres": ["rock", "intense", "metal", "power", "high energy"],
    },
    "Fear": {
        "valence": (0.00, 0.40),
        "energy": (0.60, 1.00),
        "genres": ["calm", "ambient", "soothing", "instrumental", "relaxing"],
    },
    "Surprise": {
        "valence": (0.40, 0.70),
        "energy": (0.60, 1.00),
        "genres": ["party", "electronic", "dance", "energetic", "bold"],
    },
    "Neutral": {
        "valence": (0.40, 0.60),
        "energy": (0.40, 0.60),
        "genres": ["lofi", "chill", "indie", "easy listening", "balanced"],
    },
}


def load_song_catalog():
    catalog = pd.read_csv(SONG_DATA_PATH)
    catalog = catalog.dropna(subset=["name", "artists", "valence", "energy"]).copy()

    for column in ["valence", "energy"]:
        catalog[column] = pd.to_numeric(catalog[column], errors="coerce")

    catalog = catalog.dropna(subset=["valence", "energy"])
    return catalog


SONG_CATALOG = load_song_catalog()


def get_emotion_rule(emotion):
    normalized_emotion = str(emotion).strip().title()
    return EMOTION_AUDIO_RULES.get(normalized_emotion, EMOTION_AUDIO_RULES["Neutral"])


def recommend_genres(emotion, top_n=5):
    rule = get_emotion_rule(emotion)
    return rule["genres"][:top_n]


def select_matching_songs(emotion):
    rule = get_emotion_rule(emotion)
    valence_min, valence_max = rule["valence"]
    energy_min, energy_max = rule["energy"]

    return SONG_CATALOG[
        SONG_CATALOG["valence"].between(valence_min, valence_max)
        & SONG_CATALOG["energy"].between(energy_min, energy_max)
    ]


def format_song_rows(rows):
    songs = []

    for _, row in rows.iterrows():
        title = str(row["name"]).strip()
        artist = str(row["artists"]).strip()
        query = urllib.parse.quote(f"{title} {artist}")
        songs.append(
            {
                "title": title,
                "artist": artist,
                "track_id": str(row.get("id", "")),
                "image": "",
                "spotify_search_url": f"https://open.spotify.com/search/{query}",
            }
        )

    return songs


def get_songs_from_emotion(emotion, top_n=5):
    matches = select_matching_songs(emotion)

    if matches.empty:
        chosen_rows = SONG_CATALOG.sample(n=min(top_n, len(SONG_CATALOG)))
    else:
        chosen_rows = matches.sample(n=min(top_n, len(matches)))

    return format_song_rows(chosen_rows)


def recommend_music(emotion, top_n=5):
    genres = recommend_genres(emotion, top_n=top_n)
    songs = get_songs_from_emotion(emotion, top_n=top_n)
    return genres, songs
