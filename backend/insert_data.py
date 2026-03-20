import sqlite3

conn = sqlite3.connect("music.db")
cursor = conn.cursor()

songs = [
    ("Shape of You", "Ed Sheeran", "pop", "pop"),
    ("Blinding Lights", "The Weeknd", "dance", "pop"),
    ("Someone Like You", "Adele", "sad", "acoustic"),
    ("Let Her Go", "Passenger", "sad", "acoustic"),
    ("Believer", "Imagine Dragons", "rock", "rock"),
    ("Thunder", "Imagine Dragons", "rock", "rock"),
    ("Weightless", "Ambient", "calm", "lofi"),
    ("Perfect", "Ed Sheeran", "romantic", "pop")
]

cursor.executemany("""
INSERT INTO music (title, artist, mood, genre)
VALUES (?, ?, ?, ?)
""", songs)

conn.commit()
conn.close()

print("Songs inserted successfully!")