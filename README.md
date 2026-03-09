# Emotion Detection API using CNN & Transfer Learning

## Overview
This project implements a Facial Emotion Detection System using Deep Learning.  
The model predicts human emotions from facial images using a Convolutional Neural Network (CNN) with Transfer Learning. The trained model is deployed as a REST API using FastAPI so users can upload an image and receive the predicted emotion.

## Features
- Facial emotion recognition using deep learning
- CNN model trained using MobileNetV2
- REST API built with FastAPI
- API server powered by Uvicorn
- Image preprocessing using Torchvision
- Interactive API testing through Swagger UI

## Emotion Classes
The model predicts the following emotions:
- Angry
- Disgust
- Fear
- Happy
- Sad
- Surprise
- Neutral

## Technologies Used
- Python
- PyTorch
- Torchvision
- FastAPI
- Uvicorn
- Pillow (PIL)
- Google Colab

## Project Structure
emotion-detection-project
│
├── api
│   └── emotion_api.py
│
├── model
│   └── emotion_model.pth
│
├── train_model.py
│
├── dataset
│
└── README.md

## Installation
Clone the repository:

git clone(https://github.com/springboardmentor443m-coder/Emotion-Detection-and-Music-Recommendation-System/edit/lithinkumar)
cd emotion-detection-project

Install dependencies:

pip install torch torchvision fastapi uvicorn pillow

## Running the API
Start the server:

uvicorn api.emotion_api:app --host 0.0.0.0 --port 8000

Server will run at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoint

POST /predict

Upload a facial image and the API will return the predicted emotion.

Example Response:

{
  "emotion": "Happy"
}

## Running in Google Colab
Since Google Colab runs on a remote server, the API must be exposed using ngrok.

Install ngrok:

pip install pyngrok

Expose the server:

from pyngrok import ngrok
public_url = ngrok.connect(8000)
print(public_url)

Open the generated URL in your browser.

## System Workflow

User uploads image  
↓  
FastAPI server receives image  
↓  
Image preprocessing and transformation  
↓  
CNN model predicts emotion  
↓  
API returns predicted emotion

## Future Improvements
- Real-time webcam emotion detection
- Emotion-based music recommendation system
- Web interface for uploading images
- Deployment on cloud platforms

## Author
Lithin Kumar
