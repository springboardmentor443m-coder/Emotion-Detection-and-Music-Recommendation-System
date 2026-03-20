# Emotion-Detection-and-Music-Recommendation-System

# MoodMate

MoodMate is an emotion-aware music recommendation app. It detects mood from:

- facial expression in an uploaded image or webcam capture
- user-written text

After detecting the emotion, the app recommends songs that fit that mood and stores recent results in mood history.

## Prerequisites

- Python 3.x
- internet connection only if you want Spotify-backed recommendations

## Final App Structure

- `backend/app.py`: Flask backend for image and text mood prediction
- `backend/music_recommender.py`: rule-based music recommendation logic
- `backend/text_emotion_detector.py`: text emotion pipeline
- `backend/database.py`: SQLite setup and mood history helpers
- `backend/best_model.keras`: trained facial emotion model
- `backend/music.db`: SQLite database used by the app
- `frontend/index.html`: main user interface
- `frontend/script.js`: frontend behavior and API calls
- `frontend/style.css`: frontend styling
- `data/music/data.csv`: music dataset used for recommendations
- `text/text_emotions.csv`: dataset used by the text emotion detector

## Install

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

If your system uses a different Python command, replace `python` with the correct one.

## Spotify Setup

Spotify is optional. If you configure Spotify credentials, the backend can include Spotify tracks in the recommendations.

Set these before running the backend:

```bash
set SPOTIFY_CLIENT_ID=your_spotify_client_id
set SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

For PowerShell:

```powershell
$env:SPOTIFY_CLIENT_ID="your_spotify_client_id"
$env:SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
```

If Spotify is not configured, MoodMate still returns recommendations using the local dataset and fallback songs.

## Run The Backend

From the project root:

```bash
python backend/app.py
```

Available endpoints:

- `GET /health`
- `POST /predict`
- `POST /predict-text`
- `GET /history`
- `DELETE /history`

## Run The Frontend

Open `frontend/index.html` in the browser after the backend is running.

The frontend sends requests to:

```text
http://127.0.0.1:5000
```

## Emotion Classes

The app predicts these final emotion classes:

- Angry
- Fear
- Happy
- Neutral
- Sad
- Surprise

## How The Final App Works

### Image Mood Flow

- the frontend sends an uploaded image or webcam frame to `/predict`
- the backend detects the face, preprocesses it, and predicts the emotion
- songs are recommended for that mood
- the detected mood is saved to history

### Text Mood Flow

- the frontend sends text to `/predict-text`
- the backend loads `text/text_emotions.csv`
- it trains the text classifier in memory at startup
- the classifier predicts the emotion from the input text
- songs are recommended for that mood
- the detected mood is saved to history

## Mood History

- every image or text prediction is stored in the SQLite database
- the frontend can load recent history using `GET /history`
- the frontend can clear history using `DELETE /history`

## Sample Test Inputs

You can try text inputs like:

- `I feel really happy today`
- `I feel lonely and sad`
- `I am stressed and worried about tomorrow`
- `I feel calm but slightly tired`

For image testing, use a clear front-facing face image or webcam frame.

## Without Spotify

- the app still works even if Spotify credentials are not set
- it falls back to dataset-based recommendations and local backup songs

## Notes

- The image emotion model is expected at `backend/best_model.keras`
- The text dataset is expected at `text/text_emotions.csv`
- The frontend assumes the backend runs locally on port `5000`
