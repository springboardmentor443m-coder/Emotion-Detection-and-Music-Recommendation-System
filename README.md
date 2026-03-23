# 🎵 Emotion-Based Music Recommender

An intelligent music recommendation system that detects emotions from **text** or **facial images** and suggests songs matching your mood.

## 🏛️ Architecture

```
Emotion-Music-Recommender/
│
├── backend/
│   ├── main.py               # FastAPI backend server
│   ├── music_recommender.py   # Emotion-to-music mapping logic
│   ├── text_models.py         # NLP-based emotion detection
│   ├── image_models.py        # CNN-based facial emotion detection
│   └── train_model.py         # MobileNet training script
│
├── models/
│   └── model.keras            # Trained 5-class facial emotion model
│
├── data/
│   └── song_dataset.csv       # Song metadata (valence, energy, etc.)
│
├── frontend/
│   └── app.py                 # Streamlit web UI
│
├── requirements.txt           # Project dependencies
└── README.md                  # You are here!
```

## 🔬 How It Works

### Emotion Detection

| Input Type | Model | Technique |
|-----------|-------|-----------|
| **Text** | DistilRoBERTa | NLP Sentiment Analysis via HuggingFace Transformers |
| **Image** | MobileNetV2 | Transfer Learning trained on FER-2013 Dataset |

### Emotion Categories
- 😊 **Happy** → Upbeat, energetic songs
- 😢 **Sad** → Mellow, acoustic songs
- 😠 **Angry** → Intense, heavy songs
- 😲 **Surprise** → Dynamic, varied songs
- 😐 **Neutral** → Chill, balanced songs

### Music Recommendation
Songs are recommended based on **valence** (musical positivity) and **energy** levels that correspond to the detected emotion.

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- pip

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Train the CNN Model (First Time)
```bash
python backend/train_model.py
```
This downloads the FER-2013 dataset, applies MobileNetV2 transfer learning, and saves the trained model to `models/model.keras`.

### Run the Application

**Terminal 1 — Start Backend:**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Start Frontend:**
```bash
streamlit run frontend/app.py
```

Open your browser at `http://localhost:8501`

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/detect-text` | Detect emotion from text input |
| `POST` | `/api/detect-image` | Detect emotion from image upload |
| `GET` | `/api/health` | Health check |

## 🛠️ Tech Stack

- **Backend:** FastAPI + Uvicorn
- **Frontend:** Streamlit
- **NLP Model:** HuggingFace Transformers (DistilRoBERTa)
- **CNN Model:** TensorFlow/Keras + MobileNetV2
- **Dataset:** FER-2013 (facial emotions), Custom song CSV
