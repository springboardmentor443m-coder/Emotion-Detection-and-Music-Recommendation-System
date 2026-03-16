from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

LABEL_MAP = {
    'anger':    'Angry',
    'disgust':  'Disgusted',
    'fear':     'Fearful',
    'joy':      'Happy',
    'neutral':  'Neutral',
    'sadness':  'Sad',
    'surprise': 'Surprised'
}

EMOJI_MAP = {
    'Angry':     '😠',
    'Disgusted': '🤢',
    'Fearful':   '😨',
    'Happy':     '😄',
    'Neutral':   '😐',
    'Sad':       '😢',
    'Surprised': '😮'
}

def predict_text_emotion(text):
    raw      = classifier(text)[0]
    probs    = {LABEL_MAP.get(r['label'], r['label']): round(r['score'], 4) for r in raw}
    dominant = max(probs, key=probs.get)
    return {
        'dominant':      dominant,
        'emoji':         EMOJI_MAP.get(dominant, '🤔'),
        'confidence':    probs[dominant],
        'probabilities': probs,
        'text':          text
    }