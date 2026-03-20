def map_emotion_to_mood(emotion):

    emotion_map = {
        "happy": "happy",
        "sad": "sad",
        "angry": "energetic",
        "fear": "calm",
        "surprise": "party",
        "neutral": "chill"
    }

    return emotion_map.get(emotion, "chill")