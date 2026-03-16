# 🎵 AI MoodMate  
### Emotion Detection & Music Recommendation System

AI MoodMate is an intelligent web application that detects a user's emotion from a facial image and recommends music that matches the detected mood. The system combines **Computer Vision**, **Machine Learning**, and **Music Recommendation** techniques to create a personalized music experience.

The application analyzes facial expressions using a **CNN-based emotion detection model** and recommends songs by mapping emotions to musical attributes such as **valence** and **energy** from a music dataset.

---

# 🚀 Live Demo
*(Add your deployed link here once deployed)*  

```
https://your-app-link.com
```

---

# 📌 Features

### 🧠 Emotion Detection
- Detects emotions from facial images using a **CNN-based model**
- Supported emotions:
  - Angry
  - Disgust
  - Fear
  - Happy
  - Sad
  - Surprise
  - Neutral

### 🎧 Emotion-Based Music Recommendation
Songs are recommended using **emotion-to-music mapping** based on:

- **Valence** (musical positivity)
- **Energy** (intensity of the music)

### 📷 Multiple Input Methods
Users can detect emotions using:

- Image Upload
- Live Webcam Capture

### 🎵 Spotify Music Preview
Recommended songs are displayed with embedded **Spotify players** for instant music preview.

### 🌐 Web Application
- **Frontend:** Streamlit
- **Backend:** Flask API

---

# 🏗️ System Architecture

```
User Input (Image / Webcam)
          ↓
Emotion Detection Model (CNN)
          ↓
Detected Emotion
          ↓
Music Recommendation Engine
(valence + energy filtering)
          ↓
Spotify Song Preview
          ↓
User Interface (Streamlit)
```

---

# 📊 Dataset

### Emotion Detection
- **FER-2013 Dataset**
- Used for training the CNN model for facial emotion recognition.

### Music Recommendation
- Music dataset containing song attributes such as:
  - valence
  - energy
  - tempo
  - danceability
  - genre

These features are used to map songs to emotions.

---

# 🧠 Machine Learning Model

The emotion detection system uses a **Convolutional Neural Network (CNN)** trained on facial expression data.

Model Details:

- Input size: **48 × 48 grayscale images**
- Architecture: CNN / Transfer Learning (MobileNetV2)
- Output classes: **7 emotions**

The predicted emotion is then used by the recommendation system.

---

# ⚙️ Tech Stack

### Machine Learning
- TensorFlow / Keras
- OpenCV
- NumPy
- Pandas

### Backend
- Flask API

### Frontend
- Streamlit

### Music Integration
- Spotify Embed Player

---

# 📁 Project Structure

```
Emotion-Detection-and-Music-Recommendation-System

backend
│
├── app.py
├── image_models.py
├── recommender.py

frontend
│
└── app.py

data
│
└── Music Info.csv

models
│
└── mobilenetv2.keras

requirements.txt
README.md
```

---

# 🛠️ Installation & Setup

Clone the repository:

```bash
git clone https://github.com/yourusername/AI-MoodMate.git
cd AI-MoodMate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

### Start Flask Backend

```bash
python backend/app.py
```

Backend will run on:

```
http://127.0.0.1:5000
```

---

### Start Streamlit Frontend

```bash
streamlit run frontend/app.py
```

The application will open at:

```
http://localhost:8501
```

---

# 🎯 How It Works

1️⃣ User uploads an image or captures a photo via webcam  
2️⃣ Image is sent to the Flask backend  
3️⃣ CNN model predicts the emotion  
4️⃣ Emotion is mapped to music features  
5️⃣ Songs are filtered using valence & energy  
6️⃣ Spotify preview players display recommended songs  

---

# 📈 Future Improvements

Planned enhancements include:

- Face detection using **OpenCV Haar Cascade**
- Improved emotion model accuracy (>70%)
- Real-time emotion detection from video stream
- Spotify API integration for dynamic song retrieval
- Improved UI/UX

---

# 📸 Application Preview

*(You can add screenshots here)*

```
![App Screenshot](screenshots/app_ui.png)
```

---

# 🎓 Internship Project

This project was developed as part of the **Infosys Springboard AI Internship Program**.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👩‍💻 Author

**Aditi Chaudhary**

GitHub:  
```
https://github.com/yourusername
```

LinkedIn:  
```
https://linkedin.com/in/yourprofile
```

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.