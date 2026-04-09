"""
MoodMate - Text Emotion Detection
Uses keyword scoring NLP — works fully offline, no API needed.
Maps user text to one of 7 emotions.
"""

# ── Emotion keyword dictionary ──
# Each emotion has a list of keywords
# When user types text, each matching keyword adds to that emotion's score
EMOTION_KEYWORDS = {
    "happy": [
        "happy", "joy", "joyful", "excited", "great", "wonderful", "amazing",
        "fantastic", "love", "awesome", "glad", "cheerful", "elated", "thrilled",
        "delighted", "pleased", "ecstatic", "grateful", "blessed", "smile",
        "laugh", "enjoy", "celebrate", "positive", "euphoric", "pumped",
        "overjoyed", "good", "best", "excellent", "perfect", "brilliant"
    ],
    "sad": [
        "sad", "unhappy", "depressed", "cry", "crying", "tears", "heartbreak",
        "miserable", "lonely", "grief", "loss", "miss", "disappointed", "hopeless",
        "empty", "broken", "hurt", "pain", "sorrow", "melancholy", "gloomy",
        "down", "blue", "upset", "devastated", "worthless", "crushed", "dejected",
        "alone", "abandoned", "helpless", "numb", "suffering"
    ],
    "angry": [
        "angry", "anger", "furious", "rage", "hate", "annoyed", "frustrated",
        "irritated", "mad", "livid", "outraged", "aggressive", "hostile",
        "resentful", "bitter", "enraged", "seething", "fuming", "irate",
        "boiling", "disgusted", "fed", "sick", "tired"
    ],
    "fear": [
        "afraid", "fear", "scared", "terrified", "anxious", "anxiety", "nervous",
        "panic", "dread", "worried", "worry", "frightened", "horror", "uneasy",
        "trembling", "horrified", "alarmed", "shaking", "paranoid", "petrified",
        "dreadful", "phobia", "stress", "stressed", "tense", "overwhelmed"
    ],
    "surprise": [
        "surprised", "shocked", "wow", "unexpected", "unbelievable", "astonished",
        "stunned", "speechless", "amazed", "astounded", "bewildered", "startled",
        "sudden", "sudden", "never", "unthinkable", "incredible"
    ],
    "disgust": [
        "disgusting", "gross", "revolting", "nasty", "yuck", "eww", "vile",
        "repulsed", "repulsive", "awful", "horrible", "terrible", "loathe",
        "disgusted", "sick", "nauseating", "repel", "hatred"
    ],
    "neutral": [
        "okay", "fine", "alright", "normal", "average", "meh", "whatever",
        "indifferent", "calm", "peaceful", "relaxed", "steady", "balanced",
        "so-so", "nothing", "just", "regular", "ordinary"
    ]
}

# ── Phrase patterns (stronger signals — worth more points) ──
EMOTION_PHRASES = {
    "happy": [
        "feeling good", "so happy", "really excited", "best day",
        "loving it", "on cloud nine", "over the moon", "feeling great",
        "made my day", "so excited"
    ],
    "sad": [
        "feeling sad", "so sad", "miss you", "feel empty", "feel alone",
        "cant stop crying", "feel hopeless", "feel lonely", "no one cares",
        "breaking my heart", "feel lost", "so depressed"
    ],
    "angry": [
        "so angry", "fed up", "sick of", "cant stand", "drives me crazy",
        "pissed off", "so frustrated", "makes me mad", "so annoying",
        "hate this", "really angry"
    ],
    "fear": [
        "so scared", "very anxious", "panic attack", "worried about",
        "cant sleep", "freaking out", "so nervous", "really scared",
        "feel anxious", "having anxiety"
    ],
    "surprise": [
        "mind blown", "cant believe", "did not expect", "never thought",
        "caught off guard", "totally shocked", "blew my mind"
    ],
    "disgust": [
        "makes me sick", "cant bear", "so disgusting", "turns my stomach",
        "absolutely horrible"
    ],
    "neutral": [
        "not bad", "nothing special", "just okay", "so so",
        "neither good nor bad", "feeling normal"
    ]
}

# ── Insights per emotion ──
EMOTION_INSIGHTS = {
    "happy":   "You are radiating positive energy! Great time to be productive and connect with others.",
    "sad":     "It is okay to feel sad. Allow yourself to feel it — this too shall pass. Be gentle with yourself.",
    "angry":   "Your feelings are valid. Try deep breathing or a short walk to channel this energy.",
    "fear":    "Anxiety is your mind trying to protect you. Take slow breaths and focus on what you can control.",
    "surprise":"Something unexpected caught you! Embrace the spontaneity of life.",
    "disgust": "Something is not sitting right with you. Trust your instincts — they are usually correct.",
    "neutral": "You are in a balanced state — great for focus, clear thinking, and getting things done."
}


def analyze_text_emotion(text: str) -> dict:
    """
    Detect emotion from typed or transcribed text.

    Algorithm:
    1. Convert text to lowercase
    2. Split into words
    3. Check each word against keyword lists → 2 points per match
    4. Check text for phrase patterns → 3 points per match
    5. Pick emotion with highest total score
    6. If no matches → default to neutral

    Returns:
        dict with emotion, confidence, scores, insight, method
    """

    # Step 1: Preprocess
    t     = text.lower()
    words = t.replace(",", " ").replace(".", " ").replace("!", " ") \
             .replace("?", " ").replace(";", " ").replace(":", " ").split()

    # Step 2: Score each emotion
    scores = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = 0
        # Keyword matching — 2 points each
        for keyword in keywords:
            if keyword in words:
                score += 2
        # Phrase matching — 3 points each (stronger signal)
        for phrase in EMOTION_PHRASES.get(emotion, []):
            if phrase in t:
                score += 3
        scores[emotion] = score

    # Step 3: Pick highest scoring emotion
    best_emotion = max(scores, key=scores.get)

    # Step 4: Default to neutral if no matches
    if scores[best_emotion] == 0:
        best_emotion = "neutral"
        confidence   = 0.42
    else:
        # Confidence grows with score but capped at 0.97
        confidence = min(0.55 + scores[best_emotion] * 0.06, 0.97)

    # Normalize scores to percentages
    total = sum(scores.values()) or 1
    normalized = {
        emo: round(sc / total, 3)
        for emo, sc in scores.items()
    }

    return {
        "emotion":    best_emotion,
        "confidence": round(confidence, 2),
        "scores":     normalized,
        "insight":    EMOTION_INSIGHTS[best_emotion],
        "method":     "nlp-keyword"
    }


# ── Emotion mapping (for compatibility with mentor's format) ──
# Maps fine-grained emotions to our 7 classes
EMOTION_MAPPING = {
    "joy":         "happy",
    "love":        "happy",
    "excitement":  "happy",
    "amusement":   "happy",
    "interest":    "neutral",
    "satisfaction":"neutral",
    "calmness":    "neutral",
    "sadness":     "sad",
    "anger":       "angry",
    "fear":        "fear",
    "disgust":     "disgust",
    "surprise":    "surprise"
}
