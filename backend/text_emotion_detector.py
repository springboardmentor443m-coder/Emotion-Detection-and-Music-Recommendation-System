from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression

BASE_DIR = Path(__file__).resolve().parent
TEXT_NOTEBOOK_PATH = BASE_DIR.parent / "text" / "Emotion_Detection_from_Text.ipynb"
TEXT_DATASET_PATH = BASE_DIR.parent / "text" / "text_emotions.csv"


def map_emotions(label):
    if label == "sadness":
        return "Sad"
    if label in {"joy", "love"}:
        return "Happy"
    if label == "anger":
        return "Angry"
    if label == "fear":
        return "Fear"
    if label == "surprise":
        return "Surprise"
    return "Neutral"


def train_text_model():
    if not TEXT_DATASET_PATH.exists():
        raise FileNotFoundError(f"Text dataset not found at {TEXT_DATASET_PATH}")

    df = pd.read_csv(TEXT_DATASET_PATH)
    if not {"content", "sentiment"}.issubset(df.columns):
        raise ValueError("text_emotions.csv must contain 'content' and 'sentiment' columns.")

    df = df[["content", "sentiment"]].dropna().copy()
    df["content"] = df["content"].astype(str).str.strip()
    df["sentiment"] = df["sentiment"].astype(str).str.strip().str.lower().map(map_emotions)
    df = df.dropna(subset=["sentiment"])
    df = df[df["content"] != ""]

    if df.empty:
        raise ValueError("Text emotion dataset is empty after preprocessing.")

    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(df["content"])

    transformer = TfidfTransformer()
    tfidf_features = transformer.fit_transform(counts)

    classifier = LogisticRegression(max_iter=1000)
    classifier.fit(tfidf_features, df["sentiment"])

    return {
        "vectorizer": vectorizer,
        "transformer": transformer,
        "classifier": classifier,
    }


def predict_text_emotion(model_bundle, text):
    normalized = text.strip()
    if not normalized:
        raise ValueError("Text input is empty.")

    vectorizer = model_bundle["vectorizer"]
    transformer = model_bundle["transformer"]
    classifier = model_bundle["classifier"]

    counts = vectorizer.transform([normalized])
    tfidf_features = transformer.transform(counts)
    return str(classifier.predict(tfidf_features)[0])
