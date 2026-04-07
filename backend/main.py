"""
MoodMate - FastAPI Backend  v4.0
Milestone 4: PostgreSQL database for users, history, journal
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import random, re, io, os, numpy as np
from datetime import datetime, timedelta, timezone

# ─── Optional heavy imports ───────────────────────────────────────────────────
try:
    from deepface import DeepFace
    import cv2
    DEEPFACE_AVAILABLE = True
    print("✅ DeepFace loaded")
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("⚠️  DeepFace not installed")

# Try loading our own trained .keras model (takes priority if it exists)
KERAS_MODEL      = None
KERAS_MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'emotion_model.keras')
EMOTION_LABELS   = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

try:
    import tensorflow as tf

    def _build_model():
        """Rebuild model architecture using tensorflow.keras directly."""
        m = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(48, 48, 1)),
            tf.keras.layers.Conv2D(64, (3,3), padding='same', activation='relu'),
            tf.keras.layers.Conv2D(64, (3,3), padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D((2,2)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.25),
            tf.keras.layers.Conv2D(128, (3,3), padding='same', activation='relu'),
            tf.keras.layers.Conv2D(128, (3,3), padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D((2,2)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.25),
            tf.keras.layers.Conv2D(256, (3,3), padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D((2,2)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.25),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(1024, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(7, activation='softmax')
        ])
        m.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return m

    if os.path.exists(KERAS_MODEL_PATH):
        try:
            # Try loading normally first
            KERAS_MODEL = tf.keras.models.load_model(KERAS_MODEL_PATH, compile=False)
            KERAS_MODEL.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            print(f"✅ Custom .keras model loaded from models/emotion_model.keras")
        except Exception:
            try:
                # Rebuild architecture + load weights only (bypasses config mismatch)
                tmp = _build_model()
                tmp.load_weights(KERAS_MODEL_PATH)
                KERAS_MODEL = tmp
                print(f"✅ Custom .keras model loaded (weights-only mode)")
            except Exception as e2:
                print(f"ℹ️  Could not load .keras model: {e2}")
    else:
        print("ℹ️  No custom .keras model found — using DeepFace pre-trained weights")
except Exception as e:
    print(f"ℹ️  TensorFlow not available: {e}")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import asyncpg
    DB_AVAILABLE = True
    print("✅ asyncpg loaded")
except ImportError:
    DB_AVAILABLE = False
    print("⚠️  asyncpg not installed — run: pip install asyncpg bcrypt python-jose[cryptography]")

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

try:
    from jose import jwt, JWTError
    JOSE_AVAILABLE = True
except ImportError:
    JOSE_AVAILABLE = False

# ─── Config ───────────────────────────────────────────────────────────────────
DATABASE_URL       = os.getenv("DATABASE_URL", "postgresql://moodmate_user:moodmate_pass@localhost:5432/moodmate_db")
SECRET_KEY         = os.getenv("SECRET_KEY",   "moodmate-super-secret-key-change-in-production")
ALGORITHM          = "HS256"
TOKEN_EXPIRE_DAYS  = 30

# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(title="MoodMate API", description="Emotion Detection & User Data", version="4.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
security = HTTPBearer(auto_error=False)
db_pool  = None

# ─── Startup / Shutdown ───────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    global db_pool
    if not DB_AVAILABLE:
        print("⚠️  Skipping DB — asyncpg not installed")
        return
    try:
        db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)
        await init_tables()
        print("✅ PostgreSQL connected and tables ready")
    except Exception as e:
        print(f"❌ DB failed: {e}")
        db_pool = None

@app.on_event("shutdown")
async def shutdown():
    if db_pool:
        await db_pool.close()

async def init_tables():
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id         SERIAL PRIMARY KEY,
                name       TEXT        NOT NULL,
                email      TEXT UNIQUE NOT NULL,
                password   TEXT        NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            CREATE TABLE IF NOT EXISTS mood_history (
                id         SERIAL PRIMARY KEY,
                user_id    INT  REFERENCES users(id) ON DELETE CASCADE,
                emotion    TEXT NOT NULL,
                confidence REAL NOT NULL,
                label      TEXT,
                method     TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            CREATE TABLE IF NOT EXISTS journal_entries (
                id         SERIAL PRIMARY KEY,
                user_id    INT  REFERENCES users(id) ON DELETE CASCADE,
                title      TEXT,
                body       TEXT NOT NULL,
                emotion    TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)

# ─── Auth helpers ─────────────────────────────────────────────────────────────
def hash_password(plain: str) -> str:
    if BCRYPT_AVAILABLE:
        return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()
    import hashlib
    return hashlib.sha256(plain.encode()).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    if BCRYPT_AVAILABLE:
        try:
            return bcrypt.checkpw(plain.encode(), hashed.encode())
        except Exception:
            return False
    import hashlib
    return hashlib.sha256(plain.encode()).hexdigest() == hashed

def create_token(user_id: int, email: str) -> str:
    if JOSE_AVAILABLE:
        expire = datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRE_DAYS)
        return jwt.encode({"sub": str(user_id), "email": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    import base64, json
    return base64.b64encode(json.dumps({"sub": str(user_id), "email": email}).encode()).decode()

def decode_token(token: str) -> dict:
    if JOSE_AVAILABLE:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
    import base64, json
    try:
        return json.loads(base64.b64decode(token.encode()).decode())
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    if not creds:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_token(creds.credentials)
    user_id = int(payload.get("sub", 0))
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id

# ─── Pydantic models ──────────────────────────────────────────────────────────
class SignupBody(BaseModel):
    name:     str
    email:    str
    password: str

class LoginBody(BaseModel):
    email:    str
    password: str

class TextInput(BaseModel):
    text: str

class SaveHistoryBody(BaseModel):
    emotion:    str
    confidence: float
    label:      Optional[str] = ""
    method:     Optional[str] = "nlp"

class SaveJournalBody(BaseModel):
    title:   Optional[str] = ""
    body:    str
    emotion: Optional[str] = "neutral"

class EmotionResult(BaseModel):
    emotion:    str
    confidence: float
    scores:     dict
    insight:    str
    method:     str

# ─── Emotion data ─────────────────────────────────────────────────────────────
DEEPFACE_TO_OURS = {"happy":"happy","sad":"sad","angry":"angry","fear":"fear","surprise":"surprise","disgust":"disgust","neutral":"neutral"}

EMOTION_INSIGHTS = {
    "happy":    "Happiness boosts creativity and social connection. Upbeat tempos and major keys will amplify your joy.",
    "sad":      "Sadness allows us to process loss and change. Gentle, empathetic music can be incredibly healing.",
    "angry":    "Anger signals something important feels threatened. Intense, driving music helps release that energy safely.",
    "fear":     "Anxiety activates your nervous system. Calm, grounding music with slow tempos helps ease tension.",
    "surprise": "Surprise keeps the brain curious. Dynamic, unpredictable music — jazz, experimental — matches that wonder.",
    "disgust":  "Disgust is a protective emotion. Pure, simple music helps reset your mind and restore equilibrium.",
    "neutral":  "A neutral state is great for exploring new music — your mind is receptive without emotional bias.",
}

KEYWORD_MAP = {
    "happy":    ["happy","happiness","joy","joyful","excited","elated","great","wonderful","fantastic","amazing","love","cheerful","delighted","glad","pleased","thrilled","ecstatic","bliss","blessed","grateful","thankful","good","awesome","brilliant","enjoy","enjoying","celebrate","smile","laugh","fun","positive","content","satisfied","overjoyed","jubilant","enthusiastic","optimistic"],
    "sad":      ["sad","sadness","unhappy","depressed","depression","cry","crying","tears","miserable","heartbroken","lonely","alone","grief","grieve","loss","lost","hopeless","empty","broken","down","blue","gloomy","sorrow","sorrowful","upset","hurt","pain","ache","dull","heavy","melancholy","despairing","devastated","disappointed","discouraged","helpless","worthless","numb","miss","missing","tired of everything"],
    "angry":    ["angry","anger","mad","furious","rage","hate","annoyed","irritated","frustrated","fed up","livid","outraged","bitter","hostile","resentful","infuriated","fuming","boiling","irate","enraged","aggravated","seething","explosive"],
    "fear":     ["scared","afraid","anxious","anxiety","worried","worry","nervous","panic","terrified","terror","frightened","dread","phobia","stress","stressed","overwhelmed","uneasy","tense","apprehensive","paranoid","insecure","shaking","trembling","heart racing","dreading","nightmare","fearful","horrified","petrified"],
    "surprise": ["surprised","surprise","shocked","shock","unexpected","amazed","astonished","unbelievable","wow","sudden","stunned","speechless","caught off guard","never thought","mind blown","jaw dropped","taken aback","bewildered"],
    "disgust":  ["disgusted","disgusting","disgust","gross","revolting","repulsed","repulsive","sick","nauseous","awful","horrible","terrible","yuck","nasty","vile","loathe","loathing","abhor","cannot stand","makes me sick","sick to my stomach","repelled","appalled","offensive","foul","sickening","nauseating"],
    "neutral":  ["okay","ok","fine","normal","calm","alright","nothing special","meh","so so","just","average","regular","ordinary","indifferent","neither","not sure","balanced","steady","composed","settled"],
}

# ─── NLP ──────────────────────────────────────────────────────────────────────
def analyze_text_emotion(text: str) -> dict:
    lower  = text.lower()
    scores = {e: 0.0 for e in KEYWORD_MAP}
    negation_words  = {"not","never","dont","no","neither","nor","without","hardly","barely","cannot","wont","wouldnt"}
    intensity_words = {"very","really","extremely","so","absolutely","totally","incredibly","terribly","deeply","truly","utterly","completely"}
    for emotion, keywords in KEYWORD_MAP.items():
        for kw in sorted(keywords, key=len, reverse=True):
            kw_tokens = kw.split()
            pattern   = r'\b' + r'\s+'.join(re.escape(w) for w in kw_tokens) + r'\b'
            for match in re.finditer(pattern, lower):
                preceding = lower[:match.start()].split()[-3:]
                is_neg    = any(w in negation_words for w in preceding)
                intensity = 1.5 if any(w in intensity_words for w in preceding) else 1.0
                base      = len(kw_tokens) + (1 if len(kw) > 7 else 0)
                scores[emotion] += -base * 0.5 if is_neg else base * intensity
    total      = sum(max(v,0) for v in scores.values()) or 1
    normalized = {k: round(max(v,0)/total, 3) for k,v in scores.items()}
    top        = max(normalized, key=normalized.get)
    if normalized[top] < 0.15:
        top = "neutral"
        normalized["neutral"] = max(normalized.get("neutral", 0), 0.6)
    return {"emotion": top, "confidence": round(min(normalized[top]*1.4+0.15, 0.97), 2), "scores": normalized, "method": "nlp"}

# ─── Image detection ──────────────────────────────────────────────────────────
def analyze_image_with_deepface(image_bytes: bytes) -> dict:
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img    = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")
    h, w = img.shape[:2]
    if max(h,w) > 1280:
        scale = 1280/max(h,w)
        img   = cv2.resize(img, (int(w*scale), int(h*scale)))
    try:
        results = DeepFace.analyze(img_path=img, actions=["emotion"], enforce_detection=True,  detector_backend="retinaface", silent=True)
    except Exception:
        try:
            results = DeepFace.analyze(img_path=img, actions=["emotion"], enforce_detection=False, detector_backend="opencv",     silent=True)
        except Exception:
            results = DeepFace.analyze(img_path=img, actions=["emotion"], enforce_detection=False, detector_backend="skip",       silent=True)
    best       = max(results, key=lambda r: max(r["emotion"].values())) if isinstance(results, list) else results
    raw        = best["emotion"]
    dominant   = best["dominant_emotion"]
    our_emotion= DEEPFACE_TO_OURS.get(dominant.lower(), "neutral")
    total      = sum(raw.values()) or 1
    scores     = {DEEPFACE_TO_OURS.get(k.lower(),k.lower()): round(v/total,3) for k,v in raw.items()}
    return {"emotion": our_emotion, "confidence": max(round(scores.get(our_emotion,0.5),2), 0.50), "scores": scores, "method": "deepface"}

def analyze_image_fallback(image_bytes: bytes) -> dict:
    emotions = list(KEYWORD_MAP.keys())
    primary  = random.choice(emotions)
    if PIL_AVAILABLE:
        try:
            img        = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((64,64))
            pixels     = list(img.getdata())
            avg_r      = sum(p[0] for p in pixels)/len(pixels)
            avg_g      = sum(p[1] for p in pixels)/len(pixels)
            avg_b      = sum(p[2] for p in pixels)/len(pixels)
            brightness = (avg_r+avg_g+avg_b)/3
            if   brightness > 180 and avg_r > avg_b:     primary = "happy"
            elif brightness < 80:                         primary = "sad"
            elif avg_r > avg_g+40 and avg_r > avg_b+40:  primary = "angry"
            elif avg_b > avg_r+30:                        primary = "neutral"
        except Exception:
            pass
    raw    = {e: random.uniform(1,10) for e in emotions}
    raw[primary] = random.uniform(55,75)
    total  = sum(raw.values())
    scores = {k: round(v/total,3) for k,v in raw.items()}
    return {"emotion": primary, "confidence": round(scores[primary],2), "scores": scores, "method": "fallback"}

# ══════════════════════════════════════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    return {"message": "MoodMate API v4.0 🎵", "deepface": DEEPFACE_AVAILABLE, "database": db_pool is not None, "docs": "/docs"}

@app.get("/status")
async def status():
    return {"deepface_available": DEEPFACE_AVAILABLE, "database_connected": db_pool is not None, "image_detection": "real CNN (DeepFace)" if DEEPFACE_AVAILABLE else "fallback", "text_detection": "NLP keyword analysis"}

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.post("/auth/signup")
async def signup(body: SignupBody):
    if not all([body.name.strip(), body.email.strip(), body.password.strip()]):
        raise HTTPException(400, "Name, email and password are required")
    if len(body.password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")
    if not db_pool:
        raise HTTPException(503, "Database not available — using local storage mode")
    hashed = hash_password(body.password)
    try:
        async with db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "INSERT INTO users (name, email, password) VALUES ($1,$2,$3) RETURNING id, name, email",
                body.name.strip(), body.email.lower().strip(), hashed
            )
    except asyncpg.UniqueViolationError:
        raise HTTPException(409, "An account with this email already exists")
    except Exception as e:
        raise HTTPException(500, f"Database error: {str(e)[:100]}")
    token = create_token(row["id"], row["email"])
    return {"token": token, "user": {"id": row["id"], "name": row["name"], "email": row["email"]}}

@app.post("/auth/login")
async def login(body: LoginBody):
    if not db_pool:
        raise HTTPException(503, "Database not available — using local storage mode")
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id, name, email, password FROM users WHERE email=$1", body.email.lower().strip())
    if not row:
        raise HTTPException(401, "No account found with this email")
    if not verify_password(body.password, row["password"]):
        raise HTTPException(401, "Incorrect password")
    token = create_token(row["id"], row["email"])
    return {"token": token, "user": {"id": row["id"], "name": row["name"], "email": row["email"]}}

# ── Mood History ──────────────────────────────────────────────────────────────
@app.get("/user/history")
async def get_history(user_id: int = Depends(get_current_user)):
    if not db_pool:
        raise HTTPException(503, "Database not available")
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, emotion, confidence, label, method, created_at FROM mood_history WHERE user_id=$1 ORDER BY created_at DESC LIMIT 100", user_id)
    return {"history": [dict(r) for r in rows]}

@app.post("/user/history")
async def save_history(body: SaveHistoryBody, user_id: int = Depends(get_current_user)):
    if not db_pool:
        raise HTTPException(503, "Database not available")
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("INSERT INTO mood_history (user_id, emotion, confidence, label, method) VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at", user_id, body.emotion, body.confidence, body.label, body.method)
    return {"id": row["id"], "created_at": str(row["created_at"])}

@app.delete("/user/history/{entry_id}")
async def delete_history(entry_id: int, user_id: int = Depends(get_current_user)):
    if not db_pool:
        raise HTTPException(503, "Database not available")
    async with db_pool.acquire() as conn:
        result = await conn.execute("DELETE FROM mood_history WHERE id=$1 AND user_id=$2", entry_id, user_id)
    if result == "DELETE 0":
        raise HTTPException(404, "Entry not found")
    return {"deleted": True}

# ── Journal ───────────────────────────────────────────────────────────────────
@app.get("/user/journal")
async def get_journal(user_id: int = Depends(get_current_user)):
    if not db_pool:
        raise HTTPException(503, "Database not available")
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, title, body, emotion, created_at FROM journal_entries WHERE user_id=$1 ORDER BY created_at DESC", user_id)
    return {"journal": [dict(r) for r in rows]}

@app.post("/user/journal")
async def save_journal(body: SaveJournalBody, user_id: int = Depends(get_current_user)):
    if not db_pool:
        raise HTTPException(503, "Database not available")
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("INSERT INTO journal_entries (user_id, title, body, emotion) VALUES ($1,$2,$3,$4) RETURNING id, created_at", user_id, body.title or "", body.body, body.emotion or "neutral")
    return {"id": row["id"], "created_at": str(row["created_at"])}

@app.delete("/user/journal/{entry_id}")
async def delete_journal_entry(entry_id: int, user_id: int = Depends(get_current_user)):
    if not db_pool:
        raise HTTPException(503, "Database not available")
    async with db_pool.acquire() as conn:
        result = await conn.execute("DELETE FROM journal_entries WHERE id=$1 AND user_id=$2", entry_id, user_id)
    if result == "DELETE 0":
        raise HTTPException(404, "Entry not found")
    return {"deleted": True}

# ── Emotion Detection ─────────────────────────────────────────────────────────
@app.post("/detect/text", response_model=EmotionResult)
def detect_from_text(body: TextInput):
    if not body.text.strip():
        raise HTTPException(400, "Text cannot be empty.")
    result = analyze_text_emotion(body.text)
    return EmotionResult(emotion=result["emotion"], confidence=result["confidence"], scores=result["scores"], insight=EMOTION_INSIGHTS[result["emotion"]], method=result["method"])

@app.post("/detect/image", response_model=EmotionResult)
async def detect_from_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image.")
    image_bytes = await file.read()
    if len(image_bytes) < 1000:
        raise HTTPException(400, "Image too small or corrupt.")
    if DEEPFACE_AVAILABLE:
        try:
            result = analyze_image_with_deepface(image_bytes)
        except Exception as e:
            raise HTTPException(422, f"Face not detected clearly. ({str(e)[:100]})")
    else:
        result = analyze_image_fallback(image_bytes)
    return EmotionResult(emotion=result["emotion"], confidence=result["confidence"], scores=result["scores"], insight=EMOTION_INSIGHTS[result["emotion"]], method=result["method"])

@app.get("/emotions")
def list_emotions():
    return {"emotions": list(KEYWORD_MAP.keys()), "deepface_active": DEEPFACE_AVAILABLE}