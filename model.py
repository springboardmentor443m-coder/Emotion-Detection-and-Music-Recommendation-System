import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("songs_dataset.csv")

features = [
'danceability','energy','loudness','speechiness',
'acousticness','instrumentalness','liveness','valence','tempo'
]

# SCALE FEATURES
scaler = MinMaxScaler()
df[features] = scaler.fit_transform(df[features])
df = df[df['track_name'].str.contains(r'^[A-Za-z0-9\s]+$', na=False)]

emotion_profile = {
"Happy":[0.9,0.9,0.8,0.2,0.1,0.0,0.3,0.95,0.8],
"Sad":[0.2,0.2,0.3,0.1,0.7,0.2,0.2,0.1,0.2],
"Angry":[0.5,0.95,0.6,0.2,0.05,0.0,0.3,0.4,0.9],
"Fear":[0.3,0.3,0.4,0.1,0.8,0.3,0.2,0.2,0.3],
"Surprise":[0.7,0.85,0.7,0.2,0.2,0.0,0.3,0.8,0.85],
"Neutral":[0.5,0.5,0.5,0.1,0.4,0.1,0.2,0.5,0.5]
}

def recommend_songs(emotion, n=12):

    target = np.array(emotion_profile[emotion]).reshape(1,-1)

    songs = df[features]

    similarity = cosine_similarity(target, songs)

    result = df.copy()
    result['score'] = similarity.flatten()

    result = result.sort_values('score', ascending=False)

    result = result.drop_duplicates(subset=['track_name'])

    return result[['track_name','artists']].sample(n).to_dict(orient="records")