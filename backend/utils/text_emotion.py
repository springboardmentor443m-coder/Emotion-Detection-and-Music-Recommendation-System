import re

# Weighted keyword dictionary — higher weight = stronger signal
EMOTION_KEYWORDS = {
    'Happy': {
        'words': [
            'happy','happiness','joy','joyful','excited','excitement','great','wonderful',
            'love','amazing','fantastic','good','smile','smiling','laugh','laughing',
            'fun','pleased','glad','cheerful','celebrate','celebrating','awesome',
            'excellent','superb','delighted','thrilled','ecstatic','blessed','grateful',
            'positive','enjoy','enjoying','elated','overjoyed','content','satisfied',
            'proud','lucky','brilliant','perfect','beautiful','best','incredible',
            'outstanding','magnificent','splendid','marvelous','terrific','yay',
            'woohoo','hooray','congrats','congratulations'
        ],
        'phrases': [
            'so happy','very happy','really happy','feeling happy','feel happy',
            'on top of the world','over the moon','so excited','really excited',
            'very excited','feeling great','feel great','doing great','going great',
            'so good','feeling good','feel good','really good','very good',
            'best day','good day','great day','wonderful day','amazing day',
            'love this','love it','so fun','having fun'
        ]
    },
    'Sad': {
        'words': [
            'sad','sadness','unhappy','depressed','depression','down','cry','crying',
            'tears','grief','grieving','miserable','lonely','loneliness','heartbroken',
            'upset','gloomy','sorrow','sorrowful','miss','missing','lost','hopeless',
            'empty','broken','hurt','pain','suffer','suffering','mourn','mourning',
            'regret','regretting','disappoint','disappointed','disappointment',
            'despair','despairing','melancholy','devastated','defeated','blue',
            'unfortunate','terrible','dreadful','awful','horrible','worst',
            'worthless','helpless','useless','failure','failed','alone'
        ],
        'phrases': [
            'feeling sad','feel sad','so sad','very sad','really sad',
            'feeling down','feel down','so down','really down',
            'feeling depressed','feel depressed','feeling lonely','feel lonely',
            'feeling empty','feel empty','feeling lost','feeling hopeless',
            'broken heart','heart broken','feeling blue','nothing works',
            'nothing going right','miss you','missing you','i miss',
            'no hope','gave up','giving up'
        ]
    },
    'Angry': {
        'words': [
            'angry','anger','furious','mad','rage','hate','hating','annoyed',
            'frustrated','frustration','irritated','irritating','outraged','livid',
            'unfair','stupid','idiot','idiotic','ridiculous','unacceptable',
            'useless','pathetic','disgust','disgusting','offensive','insulting',
            'insult','rude','disrespect','disrespectful','infuriated','enraged',
            'irate','hostile','bitter','resentful','violent','aggressive',
            'curse','cursing','damn','hell','terrible','horrible','awful','worst',
            'rubbish','garbage','trash','waste','disgusted','outrage'
        ],
        'phrases': [
            'so angry','very angry','really angry','feeling angry','feel angry',
            'fed up','sick of','cant stand','cannot stand','so mad','really mad',
            'very mad','drives me crazy','makes me angry','makes me mad',
            'losing my mind','losing it','had enough','enough is enough',
            'how dare','how could','this is wrong','so wrong','not fair',
            'so unfair','very unfair','i hate','really hate','absolutely hate'
        ]
    },
    'Fearful': {
        'words': [
            'scared','fear','fearful','afraid','anxious','anxiety','nervous',
            'worried','worry','worrying','panic','panicking','terrified','terror',
            'dread','dreading','horror','frightened','fright','stress','stressed',
            'stressful','threat','threatened','danger','dangerous','unsafe',
            'nightmare','phobia','tremble','trembling','shaking','uneasy',
            'concerned','apprehensive','tense','paranoid','petrified','dreadful',
            'horrified','timid','insecure','vulnerable','helpless','overwhelmed',
            'suspense','suspenseful','creepy','scary','frightening','terrifying'
        ],
        'phrases': [
            'feeling scared','feel scared','so scared','really scared','very scared',
            'feeling afraid','feel afraid','so afraid','really afraid',
            'feeling anxious','feel anxious','so anxious','really anxious',
            'feeling nervous','feel nervous','so nervous','really nervous',
            'feeling stressed','feel stressed','so stressed','really stressed',
            'scared to death','scared stiff','worried sick','so worried',
            'really worried','very worried','cannot sleep','cant sleep',
            'losing sleep','what if something','something bad','going wrong'
        ]
    },
    'Surprised': {
        'words': [
            'surprised','surprise','shocking','shocked','wow','unexpected',
            'unbelievable','astonished','astonishing','omg','sudden','suddenly',
            'whoa','incredible','stunning','speechless','startled','amazed',
            'astounded','flabbergasted','dumbfounded','staggered','bewildered',
            'extraordinary','unimaginable','unthinkable','impossible','cannot believe',
            'mind blowing','jaw dropping','never expected','out of nowhere'
        ],
        'phrases': [
            'so surprised','really surprised','very surprised','completely surprised',
            'totally surprised','oh wow','oh my god','oh my','no way',
            'cannot believe','cant believe','did not expect','did not see that coming',
            'out of nowhere','came out of nowhere','so unexpected','very unexpected',
            'never imagined','who would have thought','blown away','mind blown',
            'completely shocked','totally shocked','absolutely shocked'
        ]
    },
    'Disgusted': {
        'words': [
            'disgusting','disgust','disgusted','gross','revolting','revolted',
            'nasty','repulsive','repelled','filthy','vile','eww','yuck','yikes',
            'appalling','offensive','repugnant','foul','putrid','vulgar',
            'unpleasant','obnoxious','loathe','loathing','detest','detesting',
            'abhor','abhoring','nauseating','nauseated','sickening','sickened',
            'stomach','vomit','puke','rotten','stinky','stench','horrible',
            'atrocious','abominable','dreadful'
        ],
        'phrases': [
            'so disgusting','really disgusting','very disgusting','absolutely disgusting',
            'makes me sick','makes me want to vomit','totally gross','really gross',
            'so gross','cannot stomach','cant stomach','turns my stomach',
            'makes me cringe','so repulsive','really revolting','absolutely revolting'
        ]
    },
    'Neutral': {
        'words': [
            'okay','fine','normal','alright','nothing','just','today',
            'going','whatever','maybe','think','perhaps','sometimes',
            'usually','generally','basically','simply','average','regular',
            'ordinary','typical','standard','moderate','so so','not bad',
            'neither','neither good nor bad','indifferent'
        ],
        'phrases': [
            'just okay','pretty okay','doing okay','feeling okay','feel okay',
            'not bad','not good not bad','nothing special','nothing much',
            'same as usual','as usual','normal day','regular day'
        ]
    }
}

EMOJI_MAP = {
    'Happy':     '😄',
    'Sad':       '😢',
    'Angry':     '😠',
    'Fearful':   '😨',
    'Surprised': '😮',
    'Disgusted': '🤢',
    'Neutral':   '😐'
}

def predict_text_emotion(text):
    original = text
    lower    = text.lower()
    lower    = re.sub(r'[^\w\s]', ' ', lower)
    words    = lower.split()

    scores = {emotion: 0.0 for emotion in EMOTION_KEYWORDS}

    # Single word matching — weight 1
    for word in words:
        for emotion, data in EMOTION_KEYWORDS.items():
            if word in data['words']:
                scores[emotion] += 1.0

    # Phrase matching — weight 3 (stronger signal)
    for emotion, data in EMOTION_KEYWORDS.items():
        for phrase in data['phrases']:
            if phrase in lower:
                scores[emotion] += 3.0

    # Negation handling — flip Happy/Sad if "not" or "don't" precedes
    negations = ['not ', "don't ", "doesn't ", "didn't ", "never ", "no "]
    for neg in negations:
        if neg + 'happy' in lower or neg + 'good' in lower or neg + 'great' in lower:
            scores['Happy']  = max(0, scores['Happy'] - 2)
            scores['Sad']   += 1.5
        if neg + 'sad' in lower or neg + 'worried' in lower or neg + 'scared' in lower:
            scores['Sad']    = max(0, scores['Sad'] - 2)
            scores['Happy'] += 1.0

    total = sum(scores.values())

    # If no keywords found — return Neutral
    if total == 0:
        probs = {e: (1.0/7.0) for e in EMOTION_KEYWORDS}
        probs['Neutral'] = 0.35
        total_p = sum(probs.values())
        probs = {e: round(v/total_p, 4) for e, v in probs.items()}
        return {
            'dominant':      'Neutral',
            'emoji':         '😐',
            'confidence':    probs['Neutral'],
            'probabilities': probs,
            'text':          original
        }

    probs    = {emotion: round(count / total, 4) for emotion, count in scores.items()}
    dominant = max(probs, key=probs.get)

    return {
        'dominant':      dominant,
        'emoji':         EMOJI_MAP.get(dominant, '🤔'),
        'confidence':    probs[dominant],
        'probabilities': probs,
        'text':          original
    }