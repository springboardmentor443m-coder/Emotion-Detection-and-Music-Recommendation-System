from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import base64
import os
from model.predict import predict_from_frame
from utils.text_emotion import predict_text_emotion

app = Flask(__name__)
CORS(app)

@app.route('/api/detect/image', methods=['POST'])
def detect_image():
    data = request.json
    img_data = data.get('image', '')
    if ',' in img_data:
        img_data = img_data.split(',')[1]
    img_bytes = base64.b64decode(img_data)
    img_array = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if frame is None:
        return jsonify({'error': 'Invalid image'}), 400
    result = predict_from_frame(frame)
    return jsonify(result)

@app.route('/api/detect/live', methods=['POST'])
def detect_live():
    data = request.json
    img_data = data.get('image', '')
    if ',' in img_data:
        img_data = img_data.split(',')[1]
    img_bytes = base64.b64decode(img_data)
    img_array = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if frame is None:
        return jsonify({'error': 'Invalid image'}), 400
    result = predict_from_frame(frame)
    return jsonify(result)

@app.route('/api/detect/text', methods=['POST'])
def detect_text():
    data = request.json
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'Empty text'}), 400
    result = predict_text_emotion(text)
    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': 'VGG16-FER2013'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)