from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

LABEL_MAP = {
    'anger':   'Angry',
    'disgust': 'Disgusted',
    'fear':    'Fearful',
    'joy':     'Happy',
    'neutral': 'Neutral',
    'sadness': 'Sad',
    'surprise':'Surprised'
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
```

---

## 📄 File 6 — `.gitignore`
```
venv/
__pycache__/
*.pyc
*.pyo
*.h5
*.pkl
*.pt
.env
dataset/fer2013/
.DS_Store
Thumbs.db
*.egg-info/
dist/
build/
```

---

## 📄 File 7 — `README.md`
```
# MoodSync AI — Emotion Detection and Music Recommendation System

CNN + VGG16 Transfer Learning | FER2013 Dataset | Flask + HTML CSS JS

## Student
Branch: lithinkumar

## Features
- Live camera emotion detection
- Image upload emotion detection
- Text based emotion detection using NLP
- Mood matched music recommendations
- Real time confidence scores

## Project Structure

backend/
    app.py
    requirements.txt
    model/
        train_model.py
        predict.py
        emotion_model.h5  (generated after training)
    utils/
        text_emotion.py
frontend/
    index.html
    css/style.css
    js/app.js
dataset/
    fer2013/  (download from Kaggle)

## Setup Instructions

Step 1 - Clone the repo
git clone https://github.com/springboardmentor443m-coder/Emotion-Detection-and-Music-Recommendation-System.git
cd Emotion-Detection-and-Music-Recommendation-System
git checkout lithinkumar

Step 2 - Create virtual environment
cd backend
python -m venv venv
venv\Scripts\activate

Step 3 - Install dependencies
pip install -r requirements.txt

Step 4 - Download FER2013 dataset
Visit: https://www.kaggle.com/datasets/msambare/fer2013
Extract to: dataset/fer2013/

Step 5 - Train the model
cd backend/model
python train_model.py

Step 6 - Run the Flask server
cd backend
python app.py
Server runs at: http://127.0.0.1:5000

Step 7 - Open frontend
Open frontend/index.html in Chrome

## Model Details
Base Model     : VGG16 pretrained on ImageNet
Dataset        : FER2013 (35,887 images, 7 emotion classes)
Fine-tuned     : Last 4 convolutional blocks
Custom Head    : Dense(512) > BatchNorm > Dropout(0.5) > Dense(256) > Softmax(7)
Optimizer      : Adam lr=0.0001
Target Accuracy: 70 percent on validation set

## Emotion Classes
Angry, Disgusted, Fearful, Happy, Neutral, Sad, Surprised

## Tech Stack
Python, TensorFlow, Keras, OpenCV, Flask, HuggingFace Transformers, HTML, CSS, JavaScript