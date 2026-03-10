\#  AI — Emotion Detection + Music Recommendation



CNN + VGG16 Transfer Learning | FER2013 Dataset | Flask + Vanilla JS



\## Features

\- 📷 Live camera emotion detection

\- 🖼️ Image upload detection  

\- 💬 Text-based emotion detection (NLP)

\- 🎵 Mood-matched music recommendations



\## Setup



\### 1. Clone the repo

git clone https://github.com/YOUR\_USERNAME/moodsync-ai.git

cd moodsync-ai



\### 2. Install Python dependencies

cd backend

pip install -r requirements.txt



\### 3. Download FER2013 dataset

Get it from: https://www.kaggle.com/datasets/msambare/fer2013

Extract to: dataset/fer2013/



\### 4. Train the model

cd backend/model

python train\_model.py



\### 5. Run the Flask server

cd backend

python app.py



\### 6. Open frontend

Open frontend/index.html in your browser

Or use Live Server in VS Code



\## Model Architecture

\- Base: VGG16 pretrained on ImageNet

\- Fine-tuned layers: last 4 conv blocks

\- Custom head: Dense(512) → BN → Dropout → Dense(256) → Softmax(7)

\- Dataset: FER2013 (35,887 images, 7 classes)

\- Target accuracy: ~70%+ validation

