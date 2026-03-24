import os
import random

ROOT_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(ROOT_DIR, 'dataset', 'music_info.xlsx')

df = None

def load_dataset():
    global df
    if df is not None:
        return df
    try:
        import pandas as pd
        df = pd.read_excel(DATA_PATH)
        df.columns = df.columns.str.strip().str.lower()
        print(f"Music dataset loaded: {len(df)} tracks")
        return df
    except Exception as e:
        print(f"Dataset not found: {e} — using built-in music library")
        return None

# Emotion → audio feature ranges
# valence = positivity (0=sad, 1=happy)
# energy  = intensity  (0=calm, 1=loud/fast)
EMOTION_FILTERS = {
    'Happy':     {'valence_min':0.6, 'valence_max':1.0, 'energy_min':0.5, 'energy_max':1.0, 'sort':'valence'},
    'Sad':       {'valence_min':0.0, 'valence_max':0.4, 'energy_min':0.0, 'energy_max':0.5, 'sort':'valence_asc'},
    'Angry':     {'valence_min':0.0, 'valence_max':0.5, 'energy_min':0.7, 'energy_max':1.0, 'sort':'energy'},
    'Neutral':   {'valence_min':0.4, 'valence_max':0.7, 'energy_min':0.3, 'energy_max':0.7, 'sort':'danceability'},
    'Surprised': {'valence_min':0.5, 'valence_max':1.0, 'energy_min':0.6, 'energy_max':1.0, 'sort':'energy'},
    'Fearful':   {'valence_min':0.0, 'valence_max':0.4, 'energy_min':0.0, 'energy_max':0.6, 'sort':'valence_asc'},
    'Disgusted': {'valence_min':0.0, 'valence_max':0.4, 'energy_min':0.6, 'energy_max':1.0, 'sort':'energy'},
}

BUILTIN_DB = {
    'Happy': [
        {'title':'Good as Hell',           'artist':'Lizzo',              'duration':'3:38','valence':0.962,'energy':0.720,'spotify_url':'https://open.spotify.com/search/Good%20as%20Hell%20Lizzo'},
        {'title':'Happy',                  'artist':'Pharrell Williams',  'duration':'3:53','valence':0.963,'energy':0.815,'spotify_url':'https://open.spotify.com/search/Happy%20Pharrell%20Williams'},
        {'title':'Levitating',             'artist':'Dua Lipa',           'duration':'3:23','valence':0.821,'energy':0.762,'spotify_url':'https://open.spotify.com/search/Levitating%20Dua%20Lipa'},
        {'title':'Shake It Off',           'artist':'Taylor Swift',       'duration':'3:39','valence':0.944,'energy':0.800,'spotify_url':'https://open.spotify.com/search/Shake%20It%20Off%20Taylor%20Swift'},
        {'title':"Can't Stop the Feeling", 'artist':'Justin Timberlake',  'duration':'3:56','valence':0.930,'energy':0.782,'spotify_url':'https://open.spotify.com/search/Cant%20Stop%20the%20Feeling'},
        {'title':'Uptown Funk',            'artist':'Mark Ronson ft Bruno Mars','duration':'4:29','valence':0.940,'energy':0.857,'spotify_url':'https://open.spotify.com/search/Uptown%20Funk%20Bruno%20Mars'},
        {'title':'Dance Monkey',           'artist':'Tones and I',        'duration':'3:29','valence':0.773,'energy':0.625,'spotify_url':'https://open.spotify.com/search/Dance%20Monkey%20Tones%20and%20I'},
        {'title':'September',              'artist':'Earth Wind and Fire','duration':'3:34','valence':0.980,'energy':0.813,'spotify_url':'https://open.spotify.com/search/September%20Earth%20Wind%20and%20Fire'},
        {'title':'Walking on Sunshine',    'artist':'Katrina and the Waves','duration':'3:59','valence':0.979,'energy':0.890,'spotify_url':'https://open.spotify.com/search/Walking%20on%20Sunshine'},
        {'title':'Shape of You',           'artist':'Ed Sheeran',         'duration':'3:53','valence':0.931,'energy':0.652,'spotify_url':'https://open.spotify.com/search/Shape%20of%20You%20Ed%20Sheeran'},
    ],
    'Sad': [
        {'title':'Someone Like You',   'artist':'Adele',        'duration':'4:45','valence':0.146,'energy':0.168,'spotify_url':'https://open.spotify.com/search/Someone%20Like%20You%20Adele'},
        {'title':'Fix You',            'artist':'Coldplay',     'duration':'4:55','valence':0.181,'energy':0.252,'spotify_url':'https://open.spotify.com/search/Fix%20You%20Coldplay'},
        {'title':'The Night We Met',   'artist':'Lord Huron',   'duration':'3:28','valence':0.120,'energy':0.296,'spotify_url':'https://open.spotify.com/search/The%20Night%20We%20Met'},
        {'title':'Skinny Love',        'artist':'Bon Iver',     'duration':'3:58','valence':0.100,'energy':0.206,'spotify_url':'https://open.spotify.com/search/Skinny%20Love%20Bon%20Iver'},
        {'title':'Mad World',          'artist':'Gary Jules',   'duration':'3:07','valence':0.053,'energy':0.186,'spotify_url':'https://open.spotify.com/search/Mad%20World%20Gary%20Jules'},
        {'title':'Hurt',               'artist':'Johnny Cash',  'duration':'3:34','valence':0.040,'energy':0.163,'spotify_url':'https://open.spotify.com/search/Hurt%20Johnny%20Cash'},
        {'title':'Everybody Hurts',    'artist':'R.E.M',        'duration':'5:39','valence':0.105,'energy':0.215,'spotify_url':'https://open.spotify.com/search/Everybody%20Hurts%20REM'},
        {'title':'Let Her Go',         'artist':'Passenger',    'duration':'4:12','valence':0.312,'energy':0.294,'spotify_url':'https://open.spotify.com/search/Let%20Her%20Go%20Passenger'},
        {'title':'All I Want',         'artist':'Kodaline',     'duration':'4:49','valence':0.174,'energy':0.249,'spotify_url':'https://open.spotify.com/search/All%20I%20Want%20Kodaline'},
        {'title':'Yesterday',          'artist':'The Beatles',  'duration':'2:05','valence':0.315,'energy':0.200,'spotify_url':'https://open.spotify.com/search/Yesterday%20Beatles'},
    ],
    'Angry': [
        {'title':'Numb',                'artist':'Linkin Park',              'duration':'3:05','valence':0.183,'energy':0.897,'spotify_url':'https://open.spotify.com/search/Numb%20Linkin%20Park'},
        {'title':'Eye of the Tiger',    'artist':'Survivor',                 'duration':'4:04','valence':0.470,'energy':0.949,'spotify_url':'https://open.spotify.com/search/Eye%20of%20the%20Tiger%20Survivor'},
        {'title':'Killing in the Name', 'artist':'Rage Against the Machine', 'duration':'5:13','valence':0.232,'energy':0.981,'spotify_url':'https://open.spotify.com/search/Killing%20in%20the%20Name%20RATM'},
        {'title':'Break Stuff',         'artist':'Limp Bizkit',              'duration':'2:46','valence':0.287,'energy':0.972,'spotify_url':'https://open.spotify.com/search/Break%20Stuff%20Limp%20Bizkit'},
        {'title':'Given Up',            'artist':'Linkin Park',              'duration':'3:09','valence':0.152,'energy':0.952,'spotify_url':'https://open.spotify.com/search/Given%20Up%20Linkin%20Park'},
        {'title':'Toxicity',            'artist':'System of a Down',         'duration':'3:38','valence':0.193,'energy':0.918,'spotify_url':'https://open.spotify.com/search/Toxicity%20System%20of%20a%20Down'},
        {'title':'Faint',               'artist':'Linkin Park',              'duration':'2:42','valence':0.195,'energy':0.901,'spotify_url':'https://open.spotify.com/search/Faint%20Linkin%20Park'},
        {'title':'Animal I Have Become','artist':'Three Days Grace',         'duration':'3:40','valence':0.207,'energy':0.942,'spotify_url':'https://open.spotify.com/search/Animal%20I%20Have%20Become'},
        {'title':'In the End',          'artist':'Linkin Park',              'duration':'3:37','valence':0.219,'energy':0.542,'spotify_url':'https://open.spotify.com/search/In%20the%20End%20Linkin%20Park'},
        {'title':'Before I Forget',     'artist':'Slipknot',                 'duration':'4:08','valence':0.196,'energy':0.981,'spotify_url':'https://open.spotify.com/search/Before%20I%20Forget%20Slipknot'},
    ],
    'Neutral': [
        {'title':'Yellow',                  'artist':'Coldplay',      'duration':'4:29','valence':0.525,'energy':0.420,'spotify_url':'https://open.spotify.com/search/Yellow%20Coldplay'},
        {'title':'Budapest',               'artist':'George Ezra',   'duration':'3:14','valence':0.583,'energy':0.497,'spotify_url':'https://open.spotify.com/search/Budapest%20George%20Ezra'},
        {'title':'Coffee',                 'artist':'beabadoobee',   'duration':'1:53','valence':0.484,'energy':0.454,'spotify_url':'https://open.spotify.com/search/Coffee%20beabadoobee'},
        {'title':'Sunset Lover',           'artist':'Petit Biscuit', 'duration':'3:56','valence':0.523,'energy':0.401,'spotify_url':'https://open.spotify.com/search/Sunset%20Lover%20Petit%20Biscuit'},
        {'title':'Somewhere Only We Know', 'artist':'Keane',         'duration':'3:57','valence':0.450,'energy':0.377,'spotify_url':'https://open.spotify.com/search/Somewhere%20Only%20We%20Know%20Keane'},
        {'title':'Clocks',                 'artist':'Coldplay',      'duration':'5:07','valence':0.577,'energy':0.749,'spotify_url':'https://open.spotify.com/search/Clocks%20Coldplay'},
        {'title':'Counting Stars',         'artist':'OneRepublic',   'duration':'4:17','valence':0.629,'energy':0.643,'spotify_url':'https://open.spotify.com/search/Counting%20Stars%20OneRepublic'},
        {'title':'Wonderwall',             'artist':'Oasis',         'duration':'4:18','valence':0.409,'energy':0.408,'spotify_url':'https://open.spotify.com/search/Wonderwall%20Oasis'},
        {'title':'Africa',                 'artist':'Toto',          'duration':'4:55','valence':0.541,'energy':0.544,'spotify_url':'https://open.spotify.com/search/Africa%20Toto'},
        {'title':'Hotel California',       'artist':'Eagles',        'duration':'6:31','valence':0.489,'energy':0.511,'spotify_url':'https://open.spotify.com/search/Hotel%20California%20Eagles'},
    ],
    'Surprised': [
        {'title':'Bohemian Rhapsody',       'artist':'Queen',       'duration':'5:55','valence':0.519,'energy':0.399,'spotify_url':'https://open.spotify.com/search/Bohemian%20Rhapsody%20Queen'},
        {'title':'Mr Brightside',           'artist':'The Killers', 'duration':'3:42','valence':0.243,'energy':0.917,'spotify_url':'https://open.spotify.com/search/Mr%20Brightside%20The%20Killers'},
        {'title':'Supermassive Black Hole', 'artist':'Muse',        'duration':'3:32','valence':0.285,'energy':0.893,'spotify_url':'https://open.spotify.com/search/Supermassive%20Black%20Hole%20Muse'},
        {'title':'Starman',                 'artist':'David Bowie', 'duration':'4:16','valence':0.649,'energy':0.548,'spotify_url':'https://open.spotify.com/search/Starman%20David%20Bowie'},
        {'title':'Take On Me',              'artist':'A-ha',        'duration':'3:45','valence':0.779,'energy':0.784,'spotify_url':'https://open.spotify.com/search/Take%20On%20Me%20Aha'},
        {'title':"Don't Stop Me Now",       'artist':'Queen',       'duration':'3:29','valence':0.888,'energy':0.859,'spotify_url':'https://open.spotify.com/search/Dont%20Stop%20Me%20Now%20Queen'},
        {'title':'Jump',                    'artist':'Van Halen',   'duration':'4:00','valence':0.677,'energy':0.880,'spotify_url':'https://open.spotify.com/search/Jump%20Van%20Halen'},
        {'title':'Living on a Prayer',      'artist':'Bon Jovi',    'duration':'4:10','valence':0.687,'energy':0.872,'spotify_url':'https://open.spotify.com/search/Living%20on%20a%20Prayer%20Bon%20Jovi'},
        {'title':'I Will Survive',          'artist':'Gloria Gaynor','duration':'3:18','valence':0.797,'energy':0.815,'spotify_url':'https://open.spotify.com/search/I%20Will%20Survive%20Gloria%20Gaynor'},
        {'title':'We Will Rock You',        'artist':'Queen',       'duration':'2:01','valence':0.688,'energy':0.886,'spotify_url':'https://open.spotify.com/search/We%20Will%20Rock%20You%20Queen'},
    ],
    'Fearful': [
        {'title':'Sound of Silence', 'artist':'Simon and Garfunkel','duration':'3:05','valence':0.082,'energy':0.275,'spotify_url':'https://open.spotify.com/search/Sound%20of%20Silence%20Simon%20Garfunkel'},
        {'title':'Creep',            'artist':'Radiohead',          'duration':'3:56','valence':0.101,'energy':0.452,'spotify_url':'https://open.spotify.com/search/Creep%20Radiohead'},
        {'title':'Mad World',        'artist':'Gary Jules',         'duration':'3:07','valence':0.053,'energy':0.186,'spotify_url':'https://open.spotify.com/search/Mad%20World%20Gary%20Jules'},
        {'title':'Black',            'artist':'Pearl Jam',          'duration':'5:43','valence':0.117,'energy':0.348,'spotify_url':'https://open.spotify.com/search/Black%20Pearl%20Jam'},
        {'title':'Cemetery Gates',   'artist':'The Smiths',         'duration':'5:31','valence':0.094,'energy':0.299,'spotify_url':'https://open.spotify.com/search/Cemetery%20Gates%20Smiths'},
        {'title':'How Soon is Now',  'artist':'The Smiths',         'duration':'6:55','valence':0.063,'energy':0.407,'spotify_url':'https://open.spotify.com/search/How%20Soon%20is%20Now%20Smiths'},
        {'title':'Paranoid Android', 'artist':'Radiohead',          'duration':'6:24','valence':0.165,'energy':0.521,'spotify_url':'https://open.spotify.com/search/Paranoid%20Android%20Radiohead'},
        {'title':'Lithium',          'artist':'Nirvana',            'duration':'4:17','valence':0.485,'energy':0.656,'spotify_url':'https://open.spotify.com/search/Lithium%20Nirvana'},
        {'title':'Hurt',             'artist':'Johnny Cash',        'duration':'3:34','valence':0.040,'energy':0.163,'spotify_url':'https://open.spotify.com/search/Hurt%20Johnny%20Cash'},
        {'title':'House of the Rising Sun','artist':'The Animals',  'duration':'3:41','valence':0.179,'energy':0.423,'spotify_url':'https://open.spotify.com/search/House%20of%20the%20Rising%20Sun%20Animals'},
    ],
    'Disgusted': [
        {'title':'Toxicity',              'artist':'System of a Down','duration':'3:38','valence':0.185,'energy':0.918,'spotify_url':'https://open.spotify.com/search/Toxicity%20System%20of%20a%20Down'},
        {'title':'Chop Suey',             'artist':'System of a Down','duration':'3:30','valence':0.215,'energy':0.952,'spotify_url':'https://open.spotify.com/search/Chop%20Suey%20System%20of%20a%20Down'},
        {'title':'Cochise',               'artist':'Audioslave',      'duration':'3:44','valence':0.244,'energy':0.882,'spotify_url':'https://open.spotify.com/search/Cochise%20Audioslave'},
        {'title':'Down with the Sickness','artist':'Disturbed',       'duration':'4:37','valence':0.168,'energy':0.962,'spotify_url':'https://open.spotify.com/search/Down%20with%20the%20Sickness%20Disturbed'},
        {'title':'Headstrong',            'artist':'Trapt',           'duration':'3:42','valence':0.220,'energy':0.939,'spotify_url':'https://open.spotify.com/search/Headstrong%20Trapt'},
        {'title':'Freak on a Leash',      'artist':'Korn',            'duration':'4:08','valence':0.174,'energy':0.945,'spotify_url':'https://open.spotify.com/search/Freak%20on%20a%20Leash%20Korn'},
        {'title':'Last Resort',           'artist':'Papa Roach',      'duration':'3:20','valence':0.186,'energy':0.921,'spotify_url':'https://open.spotify.com/search/Last%20Resort%20Papa%20Roach'},
        {'title':'Come Out and Play',     'artist':'The Offspring',   'duration':'3:01','valence':0.207,'energy':0.960,'spotify_url':'https://open.spotify.com/search/Come%20Out%20and%20Play%20Offspring'},
        {'title':'Bodies',                'artist':'Drowning Pool',   'duration':'3:20','valence':0.152,'energy':0.972,'spotify_url':'https://open.spotify.com/search/Bodies%20Drowning%20Pool'},
        {'title':'Spit It Out',           'artist':'Slipknot',        'duration':'2:39','valence':0.113,'energy':0.978,'spotify_url':'https://open.spotify.com/search/Spit%20It%20Out%20Slipknot'},
    ],
}

def fmt_duration(ms):
    try:
        ms  = int(float(ms))
        m   = ms // 60000
        s   = (ms % 60000) // 1000
        return f"{m}:{s:02d}"
    except:
        return '3:30'

def calc_match(valence, energy, f):
    tv = (f['valence_min'] + f['valence_max']) / 2
    te = (f['energy_min']  + f['energy_max'])  / 2
    score = int(100 - abs(valence - tv) * 40 - abs(energy - te) * 40)
    return max(70, min(99, score))

def get_from_dataset(emotion, limit=5):
    data = load_dataset()
    if data is None:
        return None
    f = EMOTION_FILTERS.get(emotion, EMOTION_FILTERS['Neutral'])
    try:
        filtered = data[
            (data['valence'] >= f['valence_min']) &
            (data['valence'] <= f['valence_max']) &
            (data['energy']  >= f['energy_min'])  &
            (data['energy']  <= f['energy_max'])
        ].copy()

        if len(filtered) == 0:
            filtered = data[
                (data['valence'] >= f['valence_min']) &
                (data['valence'] <= f['valence_max'])
            ].copy()

        if len(filtered) == 0:
            return None

        # Sort
        sort_col = f.get('sort', 'valence')
        asc      = sort_col.endswith('_asc')
        sort_col = sort_col.replace('_asc', '')
        if sort_col not in filtered.columns:
            sort_col = 'valence'
        filtered = filtered.sort_values(sort_col, ascending=asc)

        # Sample for variety
        pool   = filtered.head(min(limit * 4, len(filtered)))
        sample = pool.sample(min(limit, len(pool)), random_state=random.randint(0, 999))

        tracks = []
        for _, row in sample.iterrows():
            title    = str(row.get('name',   row.get('title',  'Unknown')))
            artist   = str(row.get('artist', 'Unknown'))
            spot_id  = str(row.get('spotify_id', row.get('track_id', '')))
            valence  = float(row.get('valence', 0.5))
            energy   = float(row.get('energy',  0.5))
            duration = fmt_duration(row.get('duration_ms', row.get('duration_r', 210000)))

            if spot_id and spot_id not in ('nan', ''):
                spotify_url = f"https://open.spotify.com/track/{spot_id}"
            else:
                q = f"{title} {artist}".replace(' ', '%20')
                spotify_url = f"https://open.spotify.com/search/{q}"

            tracks.append({
                'title':       title,
                'artist':      artist,
                'duration':    duration,
                'preview_url': None,
                'image':       None,
                'spotify_url': spotify_url,
                'match':       f"{calc_match(valence, energy, f)}%",
                'valence':     round(valence, 3),
                'energy':      round(energy,  3),
            })

        print(f"Dataset: {len(tracks)} tracks for {emotion}")
        return tracks if tracks else None

    except Exception as e:
        print(f"Dataset error: {e}")
        return None

def get_recommendations_for_emotion(emotion, limit=5):
    emotion = emotion.capitalize()

    # Try Excel dataset first
    tracks = get_from_dataset(emotion, limit)
    if tracks and len(tracks) > 0:
        return tracks

    # Use built-in library
    library = BUILTIN_DB.get(emotion, BUILTIN_DB['Neutral'])
    # Add match score
    f = EMOTION_FILTERS.get(emotion, EMOTION_FILTERS['Neutral'])
    result = []
    for t in library[:limit]:
        t2 = dict(t)
        t2['match'] = f"{calc_match(t.get('valence',0.5), t.get('energy',0.5), f)}%"
        result.append(t2)
    return result

# Load at startup
load_dataset()
