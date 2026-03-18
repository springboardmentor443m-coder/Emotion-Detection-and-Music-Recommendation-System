from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import cv2
import base64
import os
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

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
    try:
        data     = request.json
        img_data = data.get('image', '')
        if ',' in img_data:
            img_data = img_data.split(',')[1]
        img_bytes = base64.b64decode(img_data)
        img_array = np.frombuffer(img_bytes, np.uint8)
        frame     = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({'error': 'Invalid image'}), 400

        result = predict_from_frame(frame)

        # Always attach music
        if result.get('faces') and len(result['faces']) > 0:
            dominant        = result['faces'][0]['dominant']
            result['music'] = get_recommendations_for_emotion(dominant)
        else:
            result['music'] = get_recommendations_for_emotion('Neutral')

        return jsonify(result)
    except Exception as e:
        print(f"detect_image error: {e}")
        return jsonify({'error': str(e), 'faces': [], 'music': get_recommendations_for_emotion('Neutral')}), 200

@app.route('/api/detect/live', methods=['POST'])
def detect_live():
    try:
        data     = request.json
        img_data = data.get('image', '')
        if ',' in img_data:
            img_data = img_data.split(',')[1]
        img_bytes = base64.b64decode(img_data)
        img_array = np.frombuffer(img_bytes, np.uint8)
        frame     = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({'error': 'Invalid image'}), 400

        result = predict_from_frame(frame)

        # Always attach music
        if result.get('faces') and len(result['faces']) > 0:
            dominant        = result['faces'][0]['dominant']
            result['music'] = get_recommendations_for_emotion(dominant)
        else:
            result['music'] = get_recommendations_for_emotion('Neutral')

        return jsonify(result)
    except Exception as e:
        print(f"detect_live error: {e}")
        return jsonify({'error': str(e), 'faces': [], 'music': get_recommendations_for_emotion('Neutral')}), 200

@app.route('/api/detect/text', methods=['POST'])
def detect_text():
    try:
        data   = request.json
        text   = data.get('text', '').strip()
        if not text:
            return jsonify({'error': 'Empty text'}), 400

        result          = predict_text_emotion(text)
        result['music'] = get_recommendations_for_emotion(result['dominant'])

        print(f"Text: '{text[:50]}' -> {result['dominant']} ({result['confidence']:.2f})")
        return jsonify(result)
    except Exception as e:
        print(f"detect_text error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/music/<emotion>', methods=['GET'])
def get_music(emotion):
    try:
        emotion = emotion.capitalize()
        tracks  = get_recommendations_for_emotion(emotion)
        return jsonify({'emotion': emotion, 'tracks': tracks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': 'VGG16-FER2013'})

if __name__ == '__main__':
    print("Starting MoodSync AI Flask Server...")
    app.run(debug=True, port=5000)