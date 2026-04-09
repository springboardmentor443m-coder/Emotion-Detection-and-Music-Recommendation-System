# 🎵 MoodMate — AI-Powered Emotion Detection & Music Recommendation

<div align="center">

![MoodMate Banner](https://img.shields.io/badge/MoodMate-AI%20Emotion%20Detection-7c3aed?style=for-the-badge&logo=python&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)

**Detect your emotion. Discover your music. Feel supported.**

*A full-stack AI application that detects emotions through text, photo, or camera — and recommends music that matches your mood.*

</div>

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the App](#-running-the-app)
- [How to Use](#-how-to-use)
- [Model Details](#-model-details)
- [Music Recommendation Logic](#-music-recommendation-logic)
- [API Endpoints](#-api-endpoints)
- [Environment Variables](#-environment-variables)
- [Screenshots](#-screenshots)
- [Future Scope](#-future-scope)
- [Acknowledgements](#-acknowledgements)

---

## 🧠 About the Project

MoodMate is an intelligent AI-based web application that:

1. **Detects** your current emotional state through 4 input methods
2. **Recommends** music that matches your mood from a dataset of 50,683 songs
3. **Supports** you through an empathetic AI chat companion
4. **Tracks** your emotional journey through history and journaling

> *"MoodMate — Because every emotion deserves to be heard 💜"*

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ✍️ **Text Detection** | Type how you feel — NLP keyword scoring detects emotion instantly |
| 📷 **Photo Upload** | Upload a face photo — DeepFace AI reads your expression |
| 📸 **Live Camera** | Take a selfie — emotion detected automatically |
| 🎵 **Smart Playlist** | 15 fresh songs from 50,683 tracks filtered by valence & energy |
| 🔄 **Try Again** | One click resets for a completely fresh detection |
| 🎶 **Uplift Mode** | Toggle to get happy songs when you're feeling low |
| 🤖 **AI Companion** | Claude AI chatbot for empathetic emotional support |
| 📔 **Mood Journal** | Write and save entries with emotion tags |
| 📊 **History** | Track your emotions over time with visual history |
| 🔐 **Authentication** | Secure login/signup with JWT tokens and bcrypt hashing |
| 💾 **Data Persistence** | All data saved per user — restored on next login |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Python, Streamlit |
| **Backend** | FastAPI, Uvicorn (ASGI) |
| **Face Emotion AI** | DeepFace (Facebook AI) |
| **Custom CNN Model** | TensorFlow / tf_keras |
| **Text/Voice Emotion** | NLP Keyword Scoring |
| **Voice Input** | Web Speech API (Browser) |
| **Music Dataset** | Music_Info.csv (50,683 songs) |
| **AI Chat** | Anthropic Claude API |
| **Database** | PostgreSQL (optional) + JSON file fallback |
| **Authentication** | JWT Tokens + bcrypt |
| **Data Processing** | Pandas, NumPy |
| **Image Processing** | OpenCV, Pillow |

---

## 📁 Project Structure

```
MoodMate/
│
├── streamlit_app.py          ← Main frontend application
├── Music_Info.csv            ← Music dataset (50,683 songs)
├── requirements.txt          ← Python dependencies
├── README.md
│
├── backend/
│   ├── main.py               ← FastAPI backend server
│   ├── image_models.py       ← DeepFace + CNN emotion detection
│   ├── text_models.py        ← NLP text emotion detection
│   └── recommender.py        ← Music recommendation engine
│
├── models/
│   ├── emotion_model.py      ← CNN model architecture
│   ├── emotion_model.keras   ← Trained CNN weights 
│
└── userdata/                 ← Auto-created — stores user data
    ├── accounts.json         ← User accounts
    └── [md5_hash].json       ← Per-user data files
```

---

## ✅ Prerequisites

Before running MoodMate, make sure you have:

- **Python 3.9 or higher**
- **Anaconda** (recommended) or pip
- **Chrome or Edge browser** (required for voice input)
- **Webcam** (optional, for live camera detection)

---

## 📦 Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/yourusername/MoodMate.git
cd MoodMate
```

### Step 2 — Create a Virtual Environment

```bash
# Using Anaconda (recommended)
conda create -n moodmate python=3.9
conda activate moodmate

# OR using venv
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Place the Music Dataset

Download `Music_Info.csv` and place it in the root project folder:

```
MoodMate/
└── Music_Info.csv    ← place here
```

> The dataset contains 50,683 songs with valence and energy audio feature scores used for music recommendation.

### Step 5 — Place the Trained Model

Place the trained CNN model in the models folder:

```
MoodMate/
└── models/
    └── emotion_model.keras    ← place here
    
```

> The model was trained on FER-2013 dataset and achieves **71.24% test accuracy** — exceeding human-level performance (~65%) on this benchmark.

---

## 🚀 Running the App

MoodMate runs as **two separate servers**. Open **two terminals** and run:

### Terminal 1 — Start the Backend (FastAPI)

```bash
cd backend
py -m uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Terminal 2 — Start the Frontend (Streamlit)

```bash
cd "path/to/MoodMate"
py -m streamlit run streamlit_app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Open in Browser

```
http://localhost:8501
```

> **Note:** The app works even without the backend running. Text and voice detection use local NLP, and user data is saved to JSON files automatically.

---

## 🎮 How to Use

### 1. Register / Login
- Go to **Sign Up** and create an account
- Or **Login** with existing credentials
- Your data is saved and restored automatically every session

### 2. Detect Your Emotion

Navigate to the **Detect** page and choose one of 4 methods:

**✍️ Text / Voice Tab**
- Type how you feel in the text box
- OR click the 🎤 mic button, speak, click mic again to stop
- Click **Detect My Mood**

**📷 Upload Photo Tab**
- Upload a clear photo of your face
- Click **Analyze My Expression**
- *Requires backend to be running*

**📸 Live Camera Tab**
- Click **Take Photo** in the camera widget
- Emotion is detected automatically
- *Requires backend to be running*

### 3. Your Music Playlist
- 15 songs matched to your emotion appear automatically
- Click any song card to expand and play the Spotify preview
- Click **Open on Spotify** to listen to the full song
- Toggle **🎶 Cheer me up** to get uplifting songs instead
- Click **🔄 Try Again** to detect a new mood

### 4. AI Companion
- Go to **AI Assistant** in the sidebar
- Type any message and press **Enter**
- The AI responds empathetically like a caring friend
- Full conversation history is saved per session

### 5. Mood Journal
- Go to **Journal** in the sidebar
- Write a journal entry with a title and body
- Entries are saved with emotion tags automatically

### 6. History
- Go to **History** to see all your past emotion detections
- Track your emotional patterns over time

---

## 🧠 Model Details

### Custom CNN Model

Trained from scratch on the **FER-2013** dataset:

| Detail | Value |
|--------|-------|
| Dataset | FER-2013 (Kaggle) |
| Training Images | 28,709 |
| Validation Images | 3,589 |
| Test Images | 3,589 |
| Input Size | 48×48 grayscale |
| Architecture | Conv64→Conv128→Conv256→Dense1024→Softmax7 |
| Optimizer | Adam |
| Loss | Categorical Cross-Entropy |
| Epochs | 50 |
| **Test Accuracy** | **71.24%** |
| Human Accuracy (FER-2013) | ~65% |

### 7 Emotion Classes

```
😄 Happy   😢 Sad   😠 Angry   😨 Fear
😲 Surprise   🤢 Disgust   😐 Neutral
```

## Additional Model References

The repository currently uses the compact 7-class model in models/emotion_model.py for easier version control and deployment.

For reference, higher-accuracy Keras models are also available through Google Drive. These models are larger in size (around 242 MB each), so they are not included directly in this repository.

### Reference Models

- 5-class Keras model — 70%+ accuracy
- 6-class Keras model — 70%+ accuracy
- 7-class Keras model — 70%+ accuracy

Google Drive link:  https://drive.google.com/drive/folders/1543VaOMaEslbAKUaJd3goUHNQJdtZbKk?usp=sharing

### Note

These larger reference models are shared for experimentation and comparison.  
They are not the default models used in this project because their file size makes GitHub upload and lightweight deployment harder.


## 🎵 Music Recommendation Logic

Songs are recommended using **audio feature filtering** from Music_Info.csv:

| Emotion | Valence Filter | Energy Filter |
|---------|---------------|---------------|
| 😄 Happy | > 0.6 | > 0.5 |
| 😢 Sad | < 0.4 | < 0.5 |
| 😠 Angry | < 0.4 | > 0.7 |
| 😨 Fear | < 0.4 | 0.3 – 0.7 |
| 😲 Surprise | 0.4 – 0.7 | > 0.6 |
| 🤢 Disgust | < 0.5 | 0.3 – 0.6 |
| 😐 Neutral | 0.4 – 0.6 | 0.4 – 0.6 |

- **Valence** = perceived happiness of the song (0 = very sad, 1 = very happy)
- **Energy** = perceived intensity of the song (0 = very calm, 1 = very energetic)
- **15 songs** are randomly sampled from the filtered pool every detection
- A **UUID** is generated per detection ensuring a fresh playlist every time

---

## 🔌 API Endpoints

When the FastAPI backend is running at `http://localhost:8000`:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API status check |
| `GET` | `/status` | Backend health check |
| `POST` | `/auth/signup` | Register new user |
| `POST` | `/auth/login` | Login and get JWT token |
| `POST` | `/detect/text` | Detect emotion from text |
| `POST` | `/detect/image` | Detect emotion from uploaded image |
| `POST` | `/recommend` | Get music recommendations by emotion |

---

## 🔑 Environment Variables

To enable the Claude AI chatbot, add your Anthropic API key.

Create a `.env` file in the root folder:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Or set it directly in `streamlit_app.py`:

```python
ANTHROPIC_API_KEY = "your_key_here"
```

> **Without the API key:** The chatbot still works using smart local fallback responses based on detected emotion.

> **Get your free API key at:** https://console.anthropic.com

---

## 🔧 Requirements

Key packages needed (see `requirements.txt` for full list):

```
streamlit>=1.28.0
fastapi>=0.104.0
uvicorn>=0.24.0
tf-keras>=2.15.0
deepface>=0.0.79
pandas>=2.0.0
numpy>=1.24.0
opencv-python>=4.8.0
Pillow>=10.0.0
requests>=2.31.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
```

---

## 🚀 Future Scope

- ☁️ **Cloud Deployment** — Deploy on Streamlit Cloud or AWS
- 🎧 **Spotify Integration** — Direct streaming via Spotify API
- 📱 **Mobile App** — React Native iOS and Android
- 🔊 **Voice Tone Analysis** — Detect emotion from voice pitch
- 🎯 **Better Model** — Train MobileNetV2 to achieve 75%+ accuracy
- 👥 **Community Mood Board** — Anonymous group emotion sharing

---

## 🙏 Acknowledgements

- **FER-2013 Dataset** — https://www.kaggle.com/datasets/msambare/fer2013
- **DeepFace Library** — https://github.com/serengil/deepface
- **Anthropic Claude API** — https://www.anthropic.com
- **Music Dataset** — Audio features sourced from Spotify Web API metadata
- **Streamlit** — https://streamlit.io
- **FastAPI** — https://fastapi.tiangolo.com

---

## 📄 License

This project is developed for educational purposes 
---
