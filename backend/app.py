from flask import Flask, request, jsonify
import numpy as np
import cv2

from recommender import recommend_songs_by_emotion
from image_models import predict_emotion

app = Flask(__name__)

@app.route("/recommend", methods=["POST"])
def recommend():

    file = request.files["image"]

    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    emotion = predict_emotion(img)

    songs = recommend_songs_by_emotion(emotion)

    return jsonify({
        "emotion": emotion,
        "songs": songs
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)