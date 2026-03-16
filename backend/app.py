from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import cv2
import base64
import os
from dotenv import load_dotenv

# Fix env path — load from project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

print("SPOTIFY_CLIENT_ID loaded:", os.getenv('SPOTIFY_CLIENT_ID', 'NOT FOUND')[:8]+'...')

from model.predict import predict_from_frame
from utils.text_emotion import predict_text_emotion
from utils.spotify_music import get_recommendations_for_emotion

app = Flask(__name__)
CORS(app)

FRONTEND_PATH = os.path.join(ROOT_DIR, 'frontend')

@app.route('/')
def serve_frontend():
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_PATH, path)

@app.route('/api/detect/image', methods=['POST'])
def detect_image():
    data      = request.json
    img_data  = data.get('image', '')
    if ',' in img_data:
        img_data = img_data.split(',')[1]
    img_bytes  = base64.b64decode(img_data)
    img_array  = np.frombuffer(img_bytes, np.uint8)
    frame      = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if frame is None:
        return jsonify({'error': 'Invalid image'}), 400
    result     = predict_from_frame(frame)
    if result.get('faces'):
        dominant        = result['faces'][0]['dominant']
        result['music'] = get_recommendations_for_emotion(dominant)
    return jsonify(result)

@app.route('/api/detect/live', methods=['POST'])
def detect_live():
    data      = request.json
    img_data  = data.get('image', '')
    if ',' in img_data:
        img_data = img_data.split(',')[1]
    img_bytes  = base64.b64decode(img_data)
    img_array  = np.frombuffer(img_bytes, np.uint8)
    frame      = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if frame is None:
        return jsonify({'error': 'Invalid image'}), 400
    result     = predict_from_frame(frame)
    if result.get('faces'):
        dominant        = result['faces'][0]['dominant']
        result['music'] = get_recommendations_for_emotion(dominant)
    return jsonify(result)

@app.route('/api/detect/text', methods=['POST'])
def detect_text():
    data   = request.json
    text   = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Empty text'}), 400
    result          = predict_text_emotion(text)
    result['music'] = get_recommendations_for_emotion(result['dominant'])
    return jsonify(result)

@app.route('/api/music/<emotion>', methods=['GET'])
def get_music(emotion):
    emotion = emotion.capitalize()
    tracks  = get_recommendations_for_emotion(emotion)
    return jsonify({'emotion': emotion, 'tracks': tracks})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': 'VGG16-FER2013', 'spotify': 'connected'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)