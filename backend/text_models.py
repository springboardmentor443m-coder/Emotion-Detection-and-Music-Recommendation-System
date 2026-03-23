"""
NLP-based Emotion Detection Module

Uses HuggingFace Transformers pipeline with a pre-trained
emotion classification model (DistilRoBERTa).

Supported emotions: angry, happy, neutral, sad, surprise
"""

from transformers import pipeline

# ─── Configuration ────────────────────────────────────────────────────────────

MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

# Map model output labels to our 5-class system
LABEL_MAP = {
    "anger": "angry",
    "disgust": "angry",     # Map to closest
    "fear": "sad",          # Map to closest
    "joy": "happy",
    "sadness": "sad",
    "surprise": "surprise",
    "neutral": "neutral",
}

TARGET_EMOTIONS = ["angry", "happy", "neutral", "sad", "surprise"]

# ─── Model Loading ────────────────────────────────────────────────────────────

_classifier = None


def _get_classifier():
    """Lazy-load the emotion classifier pipeline."""
    global _classifier
    if _classifier is None:
        print("[INFO] Loading NLP emotion model...")
        _classifier = pipeline(
            "text-classification",
            model=MODEL_NAME,
            top_k=None,  # Return all labels with scores
            device=-1,   # CPU (-1) or GPU (0)
        )
        print("[INFO] NLP emotion model loaded successfully.")
    return _classifier


# ─── Emotion Detection ────────────────────────────────────────────────────────

def detect_emotion_from_text(text: str) -> dict:
    """
    Detect emotion from text input.

    Args:
        text: Input text string describing the user's feelings.

    Returns:
        dict with keys:
            - emotion (str): Detected emotion label
            - confidence (float): Confidence score (0-1)
            - all_scores (dict): Scores for all emotions
    """
    if not text or not text.strip():
        return {
            "emotion": "neutral",
            "confidence": 0.0,
            "all_scores": {e: 0.0 for e in TARGET_EMOTIONS},
        }

    classifier = _get_classifier()
    results = classifier(text[:512])  # Truncate to model max length

    # Results is a list of list of dicts: [[{"label": ..., "score": ...}, ...]]
    scores = results[0]

    # Aggregate scores by our 5-class mapping
    emotion_scores = {e: 0.0 for e in TARGET_EMOTIONS}
    for item in scores:
        label = item["label"].lower()
        mapped = LABEL_MAP.get(label, "neutral")
        emotion_scores[mapped] += item["score"]

    # Normalize scores
    total = sum(emotion_scores.values())
    if total > 0:
        emotion_scores = {k: v / total for k, v in emotion_scores.items()}

    # Find top emotion
    top_emotion = max(emotion_scores, key=emotion_scores.get)
    top_confidence = emotion_scores[top_emotion]

    return {
        "emotion": top_emotion,
        "confidence": round(top_confidence, 4),
        "all_scores": {k: round(v, 4) for k, v in emotion_scores.items()},
    }


# ─── Test ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_texts = [
        "I am so happy today! Everything is wonderful!",
        "I feel really sad and alone right now.",
        "This makes me so angry! I can't believe it!",
        "Wow, I did not expect that at all! What a shock!",
        "I'm just sitting here, nothing special happening.",
        "The weather is nice but I don't feel anything particular.",
    ]

    print("=" * 60)
    print("  NLP Emotion Detection Test")
    print("=" * 60)

    for text in test_texts:
        result = detect_emotion_from_text(text)
        print(f"\nText: \"{text}\"")
        print(f"  Emotion:    {result['emotion']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  All scores: {result['all_scores']}")
