from flask import Flask, request, jsonify
from model import recommend_songs
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend():

    data = request.json
    emotion = data['emotion']

    songs = recommend_songs(emotion)

    return jsonify(songs)

if __name__ == '__main__':
    app.run(debug=True,port = 8080)