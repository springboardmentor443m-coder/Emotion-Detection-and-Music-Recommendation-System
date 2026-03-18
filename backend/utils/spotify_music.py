import os
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(ROOT_DIR, '.env'))

MUSIC_DB = {
    'Happy': [
        {'title': "Good as Hell",          'artist': 'Lizzo',             'duration': '3:38', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Good%20as%20Hell%20Lizzo',           'match': '98%'},
        {'title': "Happy",                 'artist': 'Pharrell Williams', 'duration': '3:53', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Happy%20Pharrell%20Williams',         'match': '97%'},
        {'title': "Levitating",            'artist': 'Dua Lipa',          'duration': '3:23', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Levitating%20Dua%20Lipa',            'match': '94%'},
        {'title': "Shake It Off",          'artist': 'Taylor Swift',      'duration': '3:39', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Shake%20It%20Off%20Taylor%20Swift',   'match': '91%'},
        {'title': "Can't Stop the Feeling",'artist': 'Justin Timberlake', 'duration': '3:56', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Cant%20Stop%20the%20Feeling',         'match': '88%'},
    ],
    'Sad': [
        {'title': "Someone Like You", 'artist': 'Adele',      'duration': '4:45', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Someone%20Like%20You%20Adele',   'match': '97%'},
        {'title': "Fix You",          'artist': 'Coldplay',   'duration': '4:55', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Fix%20You%20Coldplay',           'match': '95%'},
        {'title': "The Night We Met", 'artist': 'Lord Huron', 'duration': '3:28', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/The%20Night%20We%20Met',         'match': '92%'},
        {'title': "Skinny Love",      'artist': 'Bon Iver',   'duration': '3:58', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Skinny%20Love%20Bon%20Iver',     'match': '89%'},
        {'title': "Mad World",        'artist': 'Gary Jules', 'duration': '3:07', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Mad%20World%20Gary%20Jules',     'match': '86%'},
    ],
    'Angry': [
        {'title': "Numb",                'artist': 'Linkin Park',              'duration': '3:05', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Numb%20Linkin%20Park',               'match': '97%'},
        {'title': "Eye of the Tiger",    'artist': 'Survivor',                 'duration': '4:04', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Eye%20of%20the%20Tiger',             'match': '94%'},
        {'title': "Killing in the Name", 'artist': 'Rage Against the Machine', 'duration': '5:13', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Killing%20in%20the%20Name',          'match': '91%'},
        {'title': "Break Stuff",         'artist': 'Limp Bizkit',              'duration': '2:46', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Break%20Stuff%20Limp%20Bizkit',      'match': '88%'},
        {'title': "Given Up",            'artist': 'Linkin Park',              'duration': '3:09', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Given%20Up%20Linkin%20Park',         'match': '85%'},
    ],
    'Neutral': [
        {'title': "Yellow",                  'artist': 'Coldplay',      'duration': '4:29', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Yellow%20Coldplay',                  'match': '95%'},
        {'title': "Budapest",                'artist': 'George Ezra',   'duration': '3:15', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Budapest%20George%20Ezra',            'match': '92%'},
        {'title': "Coffee",                  'artist': 'beabadoobee',   'duration': '1:53', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Coffee%20beabadoobee',                'match': '90%'},
        {'title': "Sunset Lover",            'artist': 'Petit Biscuit', 'duration': '3:56', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Sunset%20Lover%20Petit%20Biscuit',    'match': '87%'},
        {'title': "Somewhere Only We Know",  'artist': 'Keane',         'duration': '3:57', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Somewhere%20Only%20We%20Know%20Keane', 'match': '84%'},
    ],
    'Surprised': [
        {'title': "Bohemian Rhapsody",       'artist': 'Queen',       'duration': '5:55', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Bohemian%20Rhapsody%20Queen',        'match': '96%'},
        {'title': "Mr Brightside",           'artist': 'The Killers', 'duration': '3:42', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Mr%20Brightside%20The%20Killers',    'match': '93%'},
        {'title': "Supermassive Black Hole", 'artist': 'Muse',        'duration': '3:32', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Supermassive%20Black%20Hole%20Muse',  'match': '90%'},
        {'title': "Starman",                 'artist': 'David Bowie', 'duration': '4:16', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Starman%20David%20Bowie',             'match': '87%'},
        {'title': "Take On Me",              'artist': 'A-ha',        'duration': '3:45', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Take%20On%20Me%20Aha',                'match': '83%'},
    ],
    'Fearful': [
        {'title': "Sound of Silence", 'artist': 'Simon and Garfunkel', 'duration': '3:05', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Sound%20of%20Silence',    'match': '96%'},
        {'title': "Creep",            'artist': 'Radiohead',           'duration': '3:56', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Creep%20Radiohead',        'match': '93%'},
        {'title': "Mad World",        'artist': 'Gary Jules',          'duration': '3:07', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Mad%20World%20Gary%20Jules', 'match': '90%'},
        {'title': "Black",            'artist': 'Pearl Jam',           'duration': '5:43', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Black%20Pearl%20Jam',      'match': '87%'},
        {'title': "Cemetery Gates",   'artist': 'The Smiths',          'duration': '5:31', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Cemetery%20Gates%20Smiths', 'match': '84%'},
    ],
    'Disgusted': [
        {'title': "Toxicity",              'artist': 'System of a Down', 'duration': '3:38', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Toxicity%20System%20of%20a%20Down',   'match': '95%'},
        {'title': "Chop Suey",             'artist': 'System of a Down', 'duration': '3:30', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Chop%20Suey%20System%20of%20a%20Down', 'match': '92%'},
        {'title': "Cochise",               'artist': 'Audioslave',       'duration': '3:44', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Cochise%20Audioslave',                'match': '89%'},
        {'title': "Down with the Sickness",'artist': 'Disturbed',        'duration': '4:37', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Down%20with%20the%20Sickness',        'match': '86%'},
        {'title': "Headstrong",            'artist': 'Trapt',            'duration': '3:42', 'preview_url': None, 'image': None, 'spotify_url': 'https://open.spotify.com/search/Headstrong%20Trapt',                  'match': '82%'},
    ],
}

def get_recommendations_for_emotion(emotion, limit=5):
    emotion = emotion.capitalize()
    tracks  = MUSIC_DB.get(emotion, MUSIC_DB['Neutral'])
    print(f"Returning {len(tracks[:limit])} Spotify tracks for emotion: {emotion}")
    return tracks[:limit]