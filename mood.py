from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from flask_cors import CORS
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)

# Load trained model
model = load_model("model.keras")

# Emotion classes 
classes = ["Angry", "Fear", "Happy", "Sad", "Surprise", "Neutral"]


def preprocess_image(img):
    """
    Preprocess image same as training
    """

    img = img.convert("L")      
    img = img.resize((128, 128))  

    img = np.array(img)
    img = img / 255.0

    img = img.reshape(1, 128, 128, 1)

    return img


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    img = Image.open(file)

    img = preprocess_image(img)

    prediction = model.predict(img)
    print(prediction)
    print()

    mood_index = np.argmax(prediction)
    print(mood_index)
    print()

    mood = classes[mood_index]

    confidence = float(np.max(prediction))

    return jsonify({
        "mood": mood,
        "confidence": confidence
    })


if __name__ == "__main__":
    app.run(port=9000, debug=True)