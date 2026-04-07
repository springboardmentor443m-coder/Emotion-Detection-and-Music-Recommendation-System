"""
MoodMate - Streamlit App v3.0
Run: py -m streamlit run streamlit_app.py
"""
import streamlit as st
import requests, time
from datetime import datetime
from PIL import Image

API        = "http://localhost:8000"
LASTFM_KEY = "2a5a893485545f8a57f9b5b72bc57c0f"

st.set_page_config(page_title="MoodMate", page_icon="🎵", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* Dark background for main app */
.stApp { background: #0d0d1a !important; }

/* Hide browser native password reveal eye — keep only Streamlit's toggle */
input[type="password"]::-ms-reveal { display: none !important; }
input[type="password"]::-ms-clear  { display: none !important; }

/* ── INPUTS: white background, black text ── */
.stTextInput > div > div > input {
  background: #ffffff !important;
  color: #111111 !important;
  border: 1.5px solid #d1d5db !important;
  border-radius: 10px !important;
  font-size: 0.95rem !important;
}
.stTextArea > div > div > textarea {
  background: #ffffff !important;
  color: #111111 !important;
  border: 1.5px solid #d1d5db !important;
  border-radius: 10px !important;
  font-size: 0.95rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: #7c3aed !important;
  box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}
input::placeholder, textarea::placeholder { color: #9ca3af !important; }

/* Input labels */
.stTextInput label, .stTextArea label { color: #e2e8f0 !important; font-weight: 500 !important; }
.stFileUploader label { color: #e2e8f0 !important; }

/* ── SIDEBAR: dark with light text ── */
div[data-testid="stSidebar"] { background: #111216 !important; }
div[data-testid="stSidebar"] p,
div[data-testid="stSidebar"] span,
div[data-testid="stSidebar"] label,
div[data-testid="stSidebar"] div { color: #e2e8f0 !important; }

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(135deg,#7c3aed,#6d28d9) !important;
  color: #ffffff !important; border: none !important;
  border-radius: 10px !important; font-weight: 600 !important;
  padding: 10px 24px !important; transition: all .2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.05) !important; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { color: #94a3b8 !important; border-radius: 8px !important; font-weight: 500 !important; }
.stTabs [aria-selected="true"] { background: rgba(124,58,237,0.35) !important; color: #ffffff !important; }

/* ── RADIO ── */
.stRadio label { color: #e2e8f0 !important; }
.stRadio > div { color: #e2e8f0 !important; }

/* ── EXPANDER ── */
details { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; }
summary { color: #e2e8f0 !important; font-weight: 600 !important; }

/* ── CHAT ── */
[data-testid="stChatMessage"] { background: rgba(255,255,255,0.04) !important; border-radius: 12px !important; }
[data-testid="stChatMessageContent"] p { color: #e2e8f0 !important; }
[data-testid="stChatInput"] textarea { background: #ffffff !important; color: #111111 !important; border-radius: 10px !important; }

/* ── ALERTS ── */
.stAlert { border-radius: 10px !important; }

/* ── LANDING CUSTOM ── */
.hero-wrap { text-align: center; padding: 70px 20px 40px; }
.grad-title { font-size: 3.2rem; font-weight: 800; background: linear-gradient(135deg,#7c3aed,#2dd4bf); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; display: block; }
.hero-sub { color: #94a3b8; font-size: 1.05rem; max-width: 560px; margin: 0 auto 32px; line-height: 1.75; display: block; }
.section-title { font-size: 2rem; font-weight: 700; color: #f1f5f9; text-align: center; margin-bottom: 8px; display: block; }
.section-sub { color: #94a3b8; text-align: center; margin-bottom: 36px; font-size: 0.95rem; display: block; }
.feat-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 28px 20px; text-align: center; }
.feat-icon { font-size: 2.2rem; margin-bottom: 12px; display: block; }
.feat-name { font-weight: 700; font-size: 1rem; color: #f1f5f9; margin-bottom: 8px; display: block; }
.feat-desc { color: #94a3b8; font-size: 0.85rem; line-height: 1.6; display: block; }
.about-box { background: rgba(124,58,237,0.08); border: 1px solid rgba(124,58,237,0.2); border-radius: 16px; padding: 36px; }
.about-text { color: #cbd5e1; line-height: 1.85; font-size: 0.97rem; margin-bottom: 16px; display: block; }

/* ── RESULT / HISTORY / JOURNAL ── */
.emotion-card { background: rgba(124,58,237,0.12); border: 1px solid rgba(124,58,237,0.3); border-radius: 16px; padding: 28px; text-align: center; margin: 12px 0; }
.insight-box { background: rgba(45,212,191,0.07); border: 1px solid rgba(45,212,191,0.2); border-radius: 12px; padding: 16px; margin: 12px 0; }
.insight-text { color: #94a3b8; display: block; }
.history-item { background: rgba(255,255,255,0.03); border-left: 3px solid #7c3aed; border-radius: 8px; padding: 10px 16px; margin: 6px 0; }
.journal-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# ── Session init ──
for k,v in [("user",None),("token",None),("history",[]),("journal",[]),("chat",[]),("last_result",None),("page","landing"),("accounts",{}),("now_playing",None),("now_playing_emotion",None),("_loaded_user",None)]:
    if k not in st.session_state: st.session_state[k] = v

# ── File-based persistence ──
import json, os, hashlib, uuid

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "userdata")
os.makedirs(DATA_DIR, exist_ok=True)

def _user_key(email):
    return hashlib.md5(email.lower().encode()).hexdigest()

def save_user_data():
    accounts_path = os.path.join(DATA_DIR, "accounts.json")
    try:
        with open(accounts_path, "w") as f:
            json.dump(st.session_state.accounts, f)
    except: pass
    user = st.session_state.get("user")
    if not user: return
    email = user.get("email","")
    if not email: return
    ukey  = _user_key(email)
    upath = os.path.join(DATA_DIR, f"{ukey}.json")
    try:
        data = {
            "email":   email,
            "name":    user.get("name",""),
            "history": st.session_state.history,
            "journal": st.session_state.journal,
            "chat":    st.session_state.get("chat", []),
        }
        with open(upath, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except: pass

def load_user_data(email):
    accounts_path = os.path.join(DATA_DIR, "accounts.json")
    if os.path.exists(accounts_path):
        try:
            with open(accounts_path) as f:
                st.session_state.accounts = json.load(f)
        except: pass
    if not email: return
    ukey  = _user_key(email)
    upath = os.path.join(DATA_DIR, f"{ukey}.json")
    if not os.path.exists(upath): return
    try:
        with open(upath) as f:
            data = json.load(f)
        st.session_state.history = data.get("history", [])
        st.session_state.journal = data.get("journal", [])
        if data.get("chat"):
            st.session_state.chat = data["chat"]
    except: pass

# Load accounts on cold start
_accounts_path = os.path.join(DATA_DIR, "accounts.json")
if os.path.exists(_accounts_path) and not st.session_state.accounts:
    try:
        with open(_accounts_path) as _f:
            st.session_state.accounts = json.load(_f)
    except: pass

# Auto-load user data when logged in but not yet loaded this session
if st.session_state.user and st.session_state._loaded_user != st.session_state.user.get("email"):
    load_user_data(st.session_state.user.get("email",""))
    st.session_state._loaded_user = st.session_state.user.get("email")

# ── Static data ──
EMOTION_META = {
    "happy":   {"emoji":"😄","color":"#fbbf24"},
    "sad":     {"emoji":"😢","color":"#60a5fa"},
    "angry":   {"emoji":"😠","color":"#f87171"},
    "fear":    {"emoji":"😨","color":"#a78bfa"},
    "surprise":{"emoji":"😲","color":"#34d399"},
    "disgust": {"emoji":"🤢","color":"#fb923c"},
    "neutral": {"emoji":"😐","color":"#94a3b8"},
}
INSIGHTS = {
    "happy":    "You're radiating positive energy! Great time to be productive and connect with others. 🌟",
    "sad":      "It's okay to feel sad. Allow yourself to feel it — this too shall pass. Be gentle with yourself. 💙",
    "angry":    "Your feelings are valid. Try deep breathing or a short walk to channel this energy. 🌬️",
    "fear":     "Anxiety is your mind trying to protect you. Take slow breaths and focus on what you can control. 🌿",
    "surprise": "Something unexpected caught you! Embrace the spontaneity of life. ✨",
    "disgust":  "Something isn't sitting right with you. Trust your instincts — they're usually correct. 🤍",
    "neutral":  "You're in a balanced state — great for focus, clear thinking, and getting things done. ⚖️",
}

# ── Load Music CSV once globally ──
import pandas as pd, os as _os, random as _random
_CSV_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "Music_Info.csv")
try:
    _music_df = pd.read_csv(_CSV_PATH)
    _music_df["spotify_url"] = _music_df["spotify_id"].apply(lambda x: f"https://open.spotify.com/track/{x}")
    _CSV_LOADED = True
except Exception as _e:
    _music_df = None
    _CSV_LOADED = False

def recommend_from_csv(emotion: str, n: int = 15, uplift: bool = False):
    """
    Recommend songs from Music_Info.csv using valence + energy audio features.
    valence = happiness (0=sad, 1=happy)
    energy  = intensity (0=calm, 1=energetic)
    """
    if not _CSV_LOADED or _music_df is None:
        return []

    df = _music_df
    emotion = emotion.lower().strip()

    if not uplift:
        # Mood-matching — music that reflects how you feel
        if emotion == "happy":
            recs = df[(df["valence"] > 0.6) & (df["energy"] > 0.5)]
        elif emotion == "sad":
            recs = df[(df["valence"] < 0.4) & (df["energy"] < 0.5)]
        elif emotion == "angry":
            recs = df[(df["valence"] < 0.4) & (df["energy"] > 0.7)]
        elif emotion in ["surprise", "surprised"]:
            recs = df[(df["valence"].between(0.4, 0.7)) & (df["energy"] > 0.6)]
        elif emotion in ["fear", "fearful"]:
            recs = df[(df["valence"] < 0.4) & (df["energy"].between(0.3, 0.7))]
        elif emotion == "disgust":
            recs = df[(df["valence"] < 0.5) & (df["energy"].between(0.3, 0.6))]
        else:  # neutral
            recs = df[(df["valence"].between(0.4, 0.6)) & (df["energy"].between(0.4, 0.6))]
    else:
        # Mood-uplifting — music to improve how you feel
        if emotion == "sad":
            recs = df[(df["valence"] > 0.6) & (df["energy"].between(0.4, 0.7))]
        elif emotion == "angry":
            recs = df[(df["valence"] > 0.5) & (df["energy"] < 0.5)]
        elif emotion in ["fear", "fearful"]:
            recs = df[(df["valence"] > 0.6) & (df["energy"].between(0.3, 0.6))]
        elif emotion == "disgust":
            recs = df[(df["valence"] > 0.6) & (df["energy"].between(0.4, 0.7))]
        elif emotion == "happy":
            recs = df[(df["valence"] > 0.6) & (df["energy"] > 0.5)]
        elif emotion in ["surprise", "surprised"]:
            recs = df[(df["valence"].between(0.5, 0.8)) & (df["energy"] > 0.6)]
        else:  # neutral
            recs = df[(df["valence"].between(0.4, 0.6)) & (df["energy"].between(0.4, 0.6))]

    if recs.empty:
        recs = df.sample(n)

    sampled = recs.sample(min(n, len(recs)))
    results = []
    for _, row in sampled.iterrows():
        results.append({
            "name":        str(row["name"]),
            "artist":      str(row["artist"]),
            "spotify_url": str(row["spotify_url"]),
            "preview_url": str(row.get("spotify_preview_url", "")),
            "valence":     round(float(row["valence"]), 2),
            "energy":      round(float(row["energy"]), 2),
        })
    return results

def show_playlist(emotion, key_prefix="", uplift=False):
    st.markdown(f"### 🎵 Your <span style='color:#a78bfa'>{emotion.title()}</span> Playlist", unsafe_allow_html=True)

    # Uplift toggle
    uplift_key = f"{key_prefix}uplift_{emotion}"
    uplift = st.toggle("🎶 Cheer me up instead of matching my mood", key=uplift_key, value=False)

    # Always use a unique cache key per detection so same emotion gives different songs
    cache_key = f"_playlist_{st.session_state.get('last_detect_id', emotion)}_{uplift}"
    if cache_key not in st.session_state:
        tracks = recommend_from_csv(emotion, n=15, uplift=uplift)
        st.session_state[cache_key] = tracks

    tracks = st.session_state[cache_key]

    if not tracks:
        st.warning("Could not load songs. Make sure Music_Info.csv is in the app folder.")
        return

    mode_label = "🎵 Mood-uplifting playlist" if uplift else "🎵 Mood-matching playlist from Music Dataset"
    st.caption(f"{mode_label} — {len(tracks)} songs")

    emojis = ["🎵","🎶","🎸","🥁","🎹","🎺","🎷","🎻","🎤","✨"]

    for i, track in enumerate(tracks):
        name    = track["name"]
        artist  = track["artist"]
        sp_url  = track["spotify_url"]
        preview = track.get("preview_url","")
        valence = track.get("valence", 0)
        energy  = track.get("energy", 0)

        label = f"{emojis[i % len(emojis)]}  **{name}** — {artist}"
        with st.expander(label, expanded=(i == 0)):
            c1, c2 = st.columns([3,1])
            with c1:
                # Spotify preview audio player if available
                if preview and preview != "nan" and preview.startswith("http"):
                    st.audio(preview, format="audio/mp3")
                else:
                    st.caption("🎧 Preview not available")
            with c2:
                st.metric("Valence", valence, help="Happiness score (0=sad, 1=happy)")
                st.metric("Energy", energy, help="Intensity score (0=calm, 1=energetic)")

            # Spotify link
            st.markdown(
                f'<a href="{sp_url}" target="_blank" style="background:#1DB954;color:white;padding:6px 14px;border-radius:20px;text-decoration:none;font-size:0.85rem;font-weight:600">'
                f'▶ Open on Spotify</a>',
                unsafe_allow_html=True
            )

    # Try Again button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Try Again — Detect a New Mood", key=f"{key_prefix}try_again", use_container_width=True):
        st.session_state.last_result      = None
        st.session_state.last_result_tab  = None
        st.session_state.now_playing      = None
        st.session_state.now_playing_emotion = None
        for k in list(st.session_state.keys()):
            if k.startswith("_playlist_"): del st.session_state[k]
        st.rerun()

def show_result(result, key_prefix=""):
    emotion = result.get("emotion","neutral")
    meta    = EMOTION_META.get(emotion, EMOTION_META["neutral"])
    conf    = int(result.get("confidence",0.5)*100)
    st.markdown(f"""
    <div class="emotion-card">
      <div style="font-size:4rem;margin-bottom:8px">{meta['emoji']}</div>
      <div style="font-size:2.2rem;font-weight:800;color:{meta['color']};margin-bottom:6px">{emotion.title()}</div>
      <div style="color:#e2e8f0;margin-bottom:14px">Confidence: {conf}%</div>
      <div style="background:rgba(255,255,255,0.08);border-radius:8px;height:8px;max-width:300px;margin:0 auto">
        <div style="background:{meta['color']};height:8px;border-radius:8px;width:{conf}%"></div>
      </div>
    </div>""", unsafe_allow_html=True)
    if result.get("insight"):
        st.markdown(f'<div class="insight-box"><span class="insight-text">💡 {result["insight"]}</span></div>', unsafe_allow_html=True)
    entry = {"emotion":emotion,"confidence":result.get("confidence",0.5),"time":datetime.now().strftime("%d %b %Y, %H:%M"),"method":result.get("method","nlp")}
    if not st.session_state.history or st.session_state.history[0].get("emotion")!=emotion:
        st.session_state.history.insert(0,entry)
        save_user_data()
    st.divider()
    show_playlist(emotion, key_prefix=key_prefix)

# ── LANDING ──
def show_landing():
    # ── Hero ──
    st.markdown("""
    <div class="hero-wrap">
      <span class="grad-title">🎵 MoodMate</span>
      <div style="color:#94a3b8;font-size:1rem;margin-bottom:16px">AI-Powered Emotion Detection &amp; Music Recommendation</div>
      <span class="hero-sub">Detect your emotions through text, voice, or facial expressions — and discover the perfect music for your mood. Track your emotional journey with AI-powered guidance.</span>
    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,1,1])
    with col1:
        if st.button("✦ Get Started Free", key="hero_get_started", use_container_width=True):
            st.session_state.page="signup"; st.rerun()
    with col2:
        if st.button("↓ See Features", key="hero_features", use_container_width=True):
            st.session_state["scroll"]="features"; st.rerun()
    with col3:
        if st.button("↓ About", key="hero_about", use_container_width=True):
            st.session_state["scroll"]="about"; st.rerun()

    # JS smooth scroll
    scroll = st.session_state.get("scroll","")
    if scroll == "features":
        st.markdown("<script>setTimeout(()=>document.getElementById('features').scrollIntoView({behavior:'smooth'}),100)</script>", unsafe_allow_html=True)
        st.session_state["scroll"] = ""
    elif scroll == "about":
        st.markdown("<script>setTimeout(()=>document.getElementById('about').scrollIntoView({behavior:'smooth'}),100)</script>", unsafe_allow_html=True)
        st.session_state["scroll"] = ""

    st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:40px 0'>", unsafe_allow_html=True)

    # ── Features ──
    st.markdown("<div id='features'></div>", unsafe_allow_html=True)
    st.markdown("<span class='section-title'>Everything you need</span>", unsafe_allow_html=True)
    st.markdown("<span class='section-sub'>MoodMate combines AI emotion detection with music therapy</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    r1c1,r1c2,r1c3 = st.columns(3)
    for col, icon, name, desc in [
        (r1c1,"🧠","Smart Detection","Detect emotions from text, photos, or live camera using deep learning AI"),
        (r1c2,"🎵","Smart Playlists","Curated music mapped to 7 distinct emotional states via Last.fm"),
        (r1c3,"📊","Mood Analytics","Track emotional trends over time with beautiful interactive charts"),
    ]:
        with col:
            st.markdown(f'<div class="feat-card"><span class="feat-icon">{icon}</span><span class="feat-name">{name}</span><span class="feat-desc">{desc}</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    r2c1,r2c2,r2c3 = st.columns(3)
    for col, icon, name, desc in [
        (r2c1,"📔","Mood Journal","Save reflections alongside your detected mood for self-awareness"),
        (r2c2,"💬","AI Assistant","Chat with your MoodMate companion for emotional support 24/7"),
        (r2c3,"🔒","Private & Secure","Your data stored locally or in PostgreSQL — always yours"),
    ]:
        with col:
            st.markdown(f'<div class="feat-card"><span class="feat-icon">{icon}</span><span class="feat-name">{name}</span><span class="feat-desc">{desc}</span></div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:40px 0'>", unsafe_allow_html=True)

    # ── About ──
    st.markdown("<div id='about'></div>", unsafe_allow_html=True)
    st.markdown("<span class='section-title'>About MoodMate</span>", unsafe_allow_html=True)
    st.markdown("<span class='section-sub'>Your personal AI companion for emotional wellness</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    _,ac,_ = st.columns([0.5,3,0.5])
    with ac:
        st.markdown("""
        <div class="about-box">
          <span class="about-text"><strong style="color:#a78bfa">What is MoodMate?</strong></span>
          <span class="about-text">MoodMate is a personal AI companion that understands how you feel. It detects your current emotion and instantly recommends music that matches your mood — helping you feel heard, supported, and less alone.</span>

          <span class="about-text" style="margin-top:18px"><strong style="color:#a78bfa">How is MoodMate useful?</strong></span>
          <span class="about-text">In today's busy world, many people struggle with their emotions silently. They feel sad, angry, or overwhelmed but have no safe space to express it. MoodMate gives you that space — privately and without any judgment.</span>
          <span class="about-text">When you're feeling low, the right music can change everything. MoodMate automatically finds songs that match exactly how you feel, so you never have to search for them yourself.</span>

          <span class="about-text" style="margin-top:18px"><strong style="color:#a78bfa">Who is it for?</strong></span>
          <span class="about-text">MoodMate is for anyone who wants to better understand their emotions, find comfort through music, or simply have a safe companion to talk to when things get difficult. Whether you're happy, sad, angry, or just feeling okay — MoodMate is always here for you. 💜</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:40px 0'>", unsafe_allow_html=True)

    # ── CTA ──
    _,c2,_ = st.columns([1,2,1])
    with c2:
        st.markdown("<div style='text-align:center;font-size:1.6rem;font-weight:700;color:#f1f5f9;margin-bottom:10px'>Ready to understand your emotions?</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;color:#94a3b8;margin-bottom:20px'>Create your free account and begin your journey.</div>", unsafe_allow_html=True)
        if st.button("✦ Sign Up Free", key="cta_signup", use_container_width=True):
            st.session_state.page="signup"; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Already have an account? Login →", key="cta_login", use_container_width=True):
            st.session_state.page="login"; st.rerun()

# ── Helpers ──
def api_headers():
    h = {"Content-Type":"application/json"}
    if st.session_state.get("token"): h["Authorization"] = f"Bearer {st.session_state.token}"
    return h

def check_backend():
    try:
        r = requests.get(f"{API}/status", timeout=0.5)
        return r.ok
    except:
        return False

def detect_text_local(text):
    t = text.lower()
    words = t.replace(","," ").replace("."," ").replace("!"," ").replace("?"," ").split()
    kws = {
        "happy":   ["happy","joy","joyful","excited","great","wonderful","amazing","fantastic","love","awesome","glad","cheerful","elated","thrilled","delighted","pleased","ecstatic","grateful","blessed","smile","laugh","enjoy","celebrate","positive","euphoric","pumped","grinning","overjoyed"],
        "sad":     ["sad","unhappy","depressed","cry","crying","tears","heartbreak","miserable","lonely","grief","loss","miss","disappointed","hopeless","empty","broken","hurt","pain","sorrow","melancholy","gloomy","down","blue","upset","devastated","worthless","crushed","dejected"],
        "angry":   ["angry","anger","furious","rage","hate","annoyed","frustrated","irritated","mad","livid","outraged","aggressive","hostile","resentful","bitter","enraged","seething","fuming","irate","boiling"],
        "fear":    ["afraid","fear","scared","terrified","anxious","anxiety","nervous","panic","dread","worried","worry","frightened","horror","uneasy","trembling","horrified","alarmed","shaking","paranoid","petrified"],
        "surprise":["surprised","shocked","wow","unexpected","unbelievable","astonished","stunned","speechless","amazed","astounded","bewildered"],
        "disgust": ["disgusting","gross","revolting","nasty","yuck","eww","vile","repulsed","repulsive","awful","horrible","terrible","loathe"],
        "neutral": ["okay","fine","alright","normal","average","meh","whatever","indifferent","calm","peaceful","relaxed","steady","balanced"],
    }
    phrases = {
        "happy":   ["feeling good","so happy","really excited","best day","loving it","on cloud nine","over the moon"],
        "sad":     ["feeling sad","so sad","miss you","feel empty","feel alone","cant stop crying","feel hopeless"],
        "angry":   ["so angry","fed up","sick of","cant stand","drives me crazy","pissed off","so frustrated"],
        "fear":    ["so scared","very anxious","panic attack","worried about","cant sleep","freaking out"],
        "surprise":["mind blown","cant believe","did not expect","never thought","caught off guard"],
        "disgust": ["makes me sick","cant bear","so disgusting","turns my stomach"],
        "neutral": ["not bad","nothing special","just okay","so so"],
    }
    scores = {}
    for emo in kws:
        s  = sum(2 for w in kws[emo] if w in words)
        s += sum(3 for p in phrases.get(emo,[]) if p in t)
        scores[emo] = s
    best = max(scores, key=scores.get)
    if scores[best] == 0: best = "neutral"
    conf = min(0.55 + scores[best]*0.06, 0.97) if scores[best]>0 else 0.42
    return {"emotion":best,"confidence":round(conf,2),"insight":INSIGHTS[best],"method":"nlp"}

# ── AUTH ──
def _hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def show_auth(mode="login"):
    _,c,_ = st.columns([1,2,1])
    with c:
        st.markdown("<div style='text-align:center;font-size:2.2rem;font-weight:800;background:linear-gradient(135deg,#7c3aed,#2dd4bf);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px'>🎵 MoodMate</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;color:#94a3b8;margin-bottom:24px'>{'Welcome back 👋' if mode=='login' else 'Create your account ✨'}</div>", unsafe_allow_html=True)

        if mode=="login":
            email = st.text_input("Email", placeholder="you@example.com", key="l_email")
            pw    = st.text_input("Password", placeholder="Your password", key="l_pw", type="password")
            if st.button("Login", use_container_width=True, key="login_btn"):
                if not email or not pw:
                    st.error("Please fill in all fields.")
                else:
                    ok = False
                    try:
                        r = requests.post(f"{API}/auth/login", json={"email":email,"password":pw}, timeout=1)
                        if r.ok:
                            st.session_state.user  = r.json()["user"]
                            st.session_state.token = r.json()["token"]
                            ok = True
                        else:
                            raise Exception(r.json().get("detail","Login failed"))
                    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                        # Backend offline — use local accounts.json
                        acc = st.session_state.accounts.get(email.lower())
                        if acc:
                            stored = acc.get("pw","")
                            # Support both hashed and plain passwords (migration)
                            if stored == _hash_pw(pw) or stored == pw:
                                st.session_state.user = {"name":acc["name"],"email":email.lower()}
                                ok = True
                            else:
                                st.error("Wrong password.")
                        else:
                            st.error("No account found with this email.")
                    except Exception as e:
                        st.error(str(e))
                    if ok:
                        email_key = st.session_state.user.get("email","")
                        load_user_data(email_key)           # ← load saved history/journal/chat
                        st.session_state._loaded_user = email_key
                        st.session_state.page = "app"
                        st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Don't have an account? Sign Up →", use_container_width=True, key="go_signup"):
                st.session_state.page="signup"; st.rerun()
        else:
            name  = st.text_input("Full Name", placeholder="Your name", key="s_name")
            email = st.text_input("Email", placeholder="you@example.com", key="s_email")
            pw    = st.text_input("Password", placeholder="Create a password", key="s_pw", type="password")
            if st.button("Create Account", use_container_width=True, key="signup_btn"):
                if not name or not email or not pw:
                    st.error("Please fill in all fields.")
                else:
                    ok = False
                    try:
                        r = requests.post(f"{API}/auth/signup", json={"name":name,"email":email,"password":pw}, timeout=1)
                        if r.ok:
                            st.session_state.user  = r.json()["user"]
                            st.session_state.token = r.json()["token"]
                            ok = True
                        else:
                            raise Exception(r.json().get("detail","Signup failed"))
                    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                        # Backend offline — save locally with hashed password
                        if email.lower() in st.session_state.accounts:
                            st.error("Email already registered. Please login.")
                        else:
                            st.session_state.accounts[email.lower()] = {
                                "name": name, "email": email.lower(), "pw": _hash_pw(pw)
                            }
                            st.session_state.user = {"name":name,"email":email.lower()}
                            ok = True
                    except Exception as e:
                        st.error(str(e))
                    if ok:
                        # New user — start with empty data, then save account
                        st.session_state.history = []
                        st.session_state.journal = []
                        st.session_state.chat    = []
                        email_key = st.session_state.user.get("email","")
                        st.session_state._loaded_user = email_key
                        save_user_data()   # save account + empty profile to disk
                        st.session_state.page = "app"
                        st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Already have an account? Login →", use_container_width=True, key="go_login"):
                st.session_state.page="login"; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Home", key="back_home", use_container_width=False):
            st.session_state.page="landing"; st.rerun()

# ── APP ──
def show_app():
    user = st.session_state.user or {}
    name = user.get("name","User")
    first = name.split()[0]

    with st.sidebar:
        st.markdown(f"<div style='font-size:1.1rem;font-weight:700;color:#111111;background:#f1f5f9;padding:10px 14px;border-radius:10px;margin-bottom:4px'>👋 Hey, {first}!</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#374151;font-size:0.8rem;margin-bottom:16px;padding:2px 4px;background:#f8fafc;border-radius:6px;padding:6px 10px'>{user.get('email','')}</div>", unsafe_allow_html=True)
        st.divider()
        page = st.radio("", ["🏠 Detect Mood","📊 History","📔 Journal","💬 Assistant"], label_visibility="collapsed")
        st.divider()
        if check_backend(): st.success("🟢 Backend connected")
        else: st.warning("🔴 Backend offline\nText detection still works!")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            save_user_data()  # ← ALWAYS save before clearing session
            for k in ["user","token","history","journal","last_result","now_playing","now_playing_emotion","_loaded_user","chat"]:
                st.session_state.pop(k, None)
            st.session_state.page = "landing"
            st.rerun()

    # ── Detect Mood ──
    if "Detect" in page:
        st.markdown("<div style='text-align:center;font-size:2.5rem;font-weight:800;background:linear-gradient(135deg,#7c3aed,#2dd4bf);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:4px'>🎵 MoodMate</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;color:#94a3b8;margin-bottom:24px'>Express yourself · Discover your music</div>", unsafe_allow_html=True)

        # Track active tab to show result only for the tab that detected
        if "active_tab" not in st.session_state:
            st.session_state.active_tab = 0

        tabs = st.tabs(["✍️ Text / Voice", "📷 Upload Photo", "📸 Live Camera"])

        # ══ TAB 0 — TEXT / VOICE ══
        with tabs[0]:
            st.markdown("<div style='color:#94a3b8;margin-bottom:6px;font-size:0.88rem'>Type how you feel, or click 🎤 to speak</div>", unsafe_allow_html=True)

            # Single unified input — mic writes into same textarea that detect button reads
            text = st.text_area(
                "",
                placeholder="e.g. I feel so happy and excited today!",
                height=130,
                key="mood_text",
                label_visibility="collapsed"
            )

            # Mic component — on stop, it fills the Streamlit textarea AND clicks detect
            mic_html = """
<style>
* { box-sizing:border-box; margin:0; padding:0; }
body { background:transparent; font-family:'Inter',sans-serif; }
#micRow { display:flex; align-items:center; gap:10px; }
#micBtn {
  width:38px; height:38px; border-radius:50%; border:none; cursor:pointer;
  background:#2d2d50; display:flex; align-items:center; justify-content:center;
  transition:background 0.15s; flex-shrink:0;
}
#micBtn:hover { background:#3d2d6e; }
#micBtn.rec   { background:#f87171; }
#micBtn svg .mf { fill:#a78bfa; }
#micBtn svg .ms { stroke:#a78bfa; }
#micBtn.rec svg .mf { fill:#fff; }
#micBtn.rec svg .ms { stroke:#fff; }
#sb { font-size:0.8rem; color:#94a3b8; }
</style>
<div id="micRow">
  <button id="micBtn" onclick="toggleMic()" title="Speak">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none">
      <rect class="mf" x="9" y="2" width="6" height="11" rx="3"/>
      <path class="ms" d="M5 11a7 7 0 0 0 14 0" stroke-width="2" stroke-linecap="round" fill="none"/>
      <line class="ms" x1="12" y1="18" x2="12" y2="21" stroke-width="2" stroke-linecap="round"/>
      <line class="ms" x1="9"  y1="21" x2="15" y2="21" stroke-width="2" stroke-linecap="round"/>
    </svg>
  </button>
  <span id="sb">🎤 Click mic to speak — words appear in the box above, then click Detect</span>
</div>
<script>
let rec=null, finalTxt="", isOn=false;
const btn=document.getElementById("micBtn");
const sb =document.getElementById("sb");

// Find the Streamlit textarea by placeholder
function getTA(){
  const all = window.parent.document.querySelectorAll("textarea");
  for(let t of all)
    if(t.placeholder && t.placeholder.includes("feel so happy")) return t;
  return null;
}

// Push value into Streamlit textarea and trigger React update
function pushToStreamlit(val){
  const ta = getTA();
  if(!ta) return;
  // Use React's internal setter to bypass read-only
  const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
    window.HTMLTextAreaElement.prototype, "value"
  ).set;
  nativeInputValueSetter.call(ta, val);
  ta.dispatchEvent(new Event("input",  { bubbles:true }));
  ta.dispatchEvent(new Event("change", { bubbles:true }));
  ta.focus();
}

function toggleMic(){
  if(!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)){
    sb.innerHTML = '<span style="color:#f87171">❌ Use Chrome or Edge for voice input</span>';
    return;
  }
  isOn ? stopRec() : startRec();
}

function startRec(){
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  rec = new SR();
  rec.continuous     = true;
  rec.interimResults = true;
  rec.lang           = "en-US";

  const ta = getTA();
  finalTxt = ta && ta.value.trim() ? ta.value.trim() + " " : "";

  btn.classList.add("rec");
  sb.innerHTML = '<span style="color:#f87171">🔴 Listening… click mic to stop</span>';
  isOn = true;

  rec.onresult = (e) => {
    let interim = "", acc = finalTxt;
    for(let i = e.resultIndex; i < e.results.length; i++){
      if(e.results[i].isFinal) acc += e.results[i][0].transcript + " ";
      else interim += e.results[i][0].transcript;
    }
    finalTxt = acc;
    pushToStreamlit((finalTxt + interim).trim());
  };

  rec.onerror = (e) => {
    sb.innerHTML = '<span style="color:#f87171">Mic error: ' + e.error + '</span>';
    stopRec();
  };

  rec.onend = () => { if(isOn) rec.start(); };
  rec.start();
}

function stopRec(){
  isOn = false;
  if(rec){ rec.onend = null; rec.stop(); }
  btn.classList.remove("rec");

  const ta = getTA();
  const val = ta ? ta.value.trim() : "";

  if(val){
    sb.innerHTML = '<span style="color:#34d399">✅ Got it! Now click Detect My Mood ↓</span>';
    // Push final value one more time to make sure Streamlit has it
    pushToStreamlit(val);
    setTimeout(()=>{
      sb.innerHTML = '<span style="color:#94a3b8">🎤 Click mic to speak again</span>';
    }, 5000);
  } else {
    sb.innerHTML = '<span style="color:#94a3b8">Nothing captured — try again</span>';
  }
}
</script>
"""
            st.components.v1.html(mic_html, height=48)

            if st.button("🔍 Detect My Mood", key="detect_text_btn", use_container_width=True):
                t = text.strip()
                if not t:
                    st.warning("⚠️ Please type something or use the 🎤 mic above.")
                else:
                    with st.spinner("Analyzing your mood..."):
                        try:
                            r = requests.post(f"{API}/detect/text", json={"text": t}, timeout=1, headers=api_headers())
                            result = r.json() if r.ok else detect_text_local(t)
                        except Exception:
                            result = detect_text_local(t)
                        result.setdefault("insight", INSIGHTS.get(result.get("emotion","neutral"),""))
                        for k in list(st.session_state.keys()):
                            if k.startswith("_playlist_"): del st.session_state[k]
                        st.session_state.update(
                            now_playing=None, now_playing_emotion=None,
                            last_result=result, last_result_tab="text"
                        )
                        st.session_state.last_detect_id = str(uuid.uuid4())
                    st.rerun()

        # ══ TAB 1 — UPLOAD PHOTO ══
        with tabs[1]:
            st.markdown("<div style='color:#94a3b8;margin-bottom:8px;font-size:0.88rem'>📷 Upload a clear photo of your face — DeepFace AI will read your expression</div>", unsafe_allow_html=True)
            uploaded = st.file_uploader("Upload photo", type=["jpg","jpeg","png"], key="photo_up", label_visibility="collapsed")
            if uploaded:
                st.image(Image.open(uploaded), width=280, caption="Your photo")
                if st.button("🔍 Analyze My Expression", key="analyze_photo_btn", use_container_width=True):
                    with st.spinner("Detecting emotion from face..."):
                        try:
                            uploaded.seek(0)
                            files = {"file": (uploaded.name, uploaded.read(), uploaded.type or "image/jpeg")}
                            r = requests.post(f"{API}/detect/image", files=files, timeout=15)
                            if r.ok:
                                result = r.json()
                                result.setdefault("insight", INSIGHTS.get(result.get("emotion","neutral"),""))
                                for k in list(st.session_state.keys()):
                                    if k.startswith("_playlist_"): del st.session_state[k]
                                st.session_state.update(now_playing=None, now_playing_emotion=None,
                                                        last_result=result, last_result_tab="photo")
                                st.session_state.last_detect_id = str(uuid.uuid4())
                                st.session_state.active_tab = 1
                            elif r.status_code == 422:
                                st.error("😕 Face not detected. Use a well-lit photo showing your full face.")
                            else:
                                st.error("Detection failed. Try again.")
                        except requests.exceptions.ConnectionError:
                            st.warning("⚠️ Backend not running. Run: cd backend && py -m uvicorn main:app --reload")
                        except Exception as e:
                            st.error(f"Error: {e}")
            else:
                st.markdown("""
                <div style='text-align:center;padding:40px 20px;color:#475569;font-size:0.9rem'>
                  <div style='font-size:3rem;margin-bottom:12px'>📷</div>
                  Upload a photo of your face above<br>then click Analyze
                </div>""", unsafe_allow_html=True)

        # ══ TAB 2 — LIVE CAMERA ══
        with tabs[2]:
            st.markdown("<div style='color:#94a3b8;margin-bottom:4px;font-size:0.88rem'>📸 Click <strong>Take photo</strong> below — your emotion is detected automatically</div>", unsafe_allow_html=True)
            st.markdown("<div style='color:#64748b;font-size:0.8rem;margin-bottom:10px'>💡 Tip: Good lighting + face the camera directly</div>", unsafe_allow_html=True)
            cam = st.camera_input("", key="cam_snap", label_visibility="collapsed")
            if cam:
                with st.spinner("Detecting your emotion..."):
                    final_result = None
                    try:
                        files = {"file": ("capture.jpg", cam.getvalue(), "image/jpeg")}
                        r = requests.post(f"{API}/detect/image", files=files, timeout=10)
                        if r.ok:
                            final_result = r.json()
                            final_result.setdefault("insight", INSIGHTS.get(final_result.get("emotion","neutral"),""))
                            final_result["method"] = "deepface"
                        elif r.status_code == 422:
                            st.warning("😕 Face not clear — try better lighting.")
                    except: pass
                    if not final_result:
                        try:
                            from PIL import Image as PILImage
                            import io as _io
                            pil = PILImage.open(_io.BytesIO(cam.getvalue())).convert("L")
                            px  = list(pil.getdata())
                            br  = sum(px)/len(px)
                            ct  = (sum((p-br)**2 for p in px)/len(px))**0.5
                            if   br>155 and ct>40: emo,conf = "happy",0.72
                            elif br>130:           emo,conf = "neutral",0.65
                            elif br>100 and ct>50: emo,conf = "surprise",0.62
                            elif br>80:            emo,conf = "sad",0.63
                            else:                  emo,conf = "neutral",0.58
                        except: emo,conf = "neutral",0.55
                        final_result = {"emotion":emo,"confidence":conf,
                                        "insight":INSIGHTS[emo],"method":"local"}
                    for k in list(st.session_state.keys()):
                        if k.startswith("_playlist_"): del st.session_state[k]
                    st.session_state.update(now_playing=None, now_playing_emotion=None,
                                            last_result=final_result, last_result_tab="camera")
                    st.session_state.last_detect_id = str(uuid.uuid4())
                    st.session_state.active_tab = 2

        # ── Result + Playlist — only show for the tab that detected ──
        if st.session_state.last_result:
            active = st.session_state.get("last_result_tab", "")
            # Show result only on the matching tab by checking which tab is rendered
            # We use a per-tab result render inside each tab's with block below
            pass

        # Render results inside each tab so switching tabs hides the other result
        with tabs[0]:
            if st.session_state.last_result and st.session_state.get("last_result_tab") == "text":
                st.divider()
                show_result(st.session_state.last_result, key_prefix="text_")

        with tabs[1]:
            if st.session_state.last_result and st.session_state.get("last_result_tab") == "photo":
                st.divider()
                show_result(st.session_state.last_result, key_prefix="photo_")

        with tabs[2]:
            if st.session_state.last_result and st.session_state.get("last_result_tab") == "camera":
                st.divider()
                show_result(st.session_state.last_result, key_prefix="camera_")

    # ── History ──
    elif "History" in page:
        st.markdown("<h2 style='color:#e2e8f0'>📊 Mood History</h2>", unsafe_allow_html=True)
        if not st.session_state.history:
            st.info("No mood history yet. Detect your mood first!")
        else:
            from collections import Counter
            counts = Counter(h["emotion"] for h in st.session_state.history)
            st.markdown("<div style='color:#e2e8f0;font-weight:600;margin-bottom:8px'>Emotion Distribution</div>", unsafe_allow_html=True)
            st.bar_chart(counts)
            st.markdown("<div style='color:#e2e8f0;font-weight:600;margin:16px 0 8px'>Recent Detections</div>", unsafe_allow_html=True)
            for h in st.session_state.history[:20]:
                meta = EMOTION_META.get(h["emotion"],EMOTION_META["neutral"])
                st.markdown(f"""<div class="history-item"><span style='font-size:1.2rem'>{meta['emoji']}</span> <strong style='color:{meta['color']}'>{h['emotion'].title()}</strong> <span style='color:#94a3b8'>&nbsp;·&nbsp; {int(h['confidence']*100)}% confidence &nbsp;·&nbsp; {h['time']}</span></div>""", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑 Clear History"):
                st.session_state.history=[]; save_user_data(); st.rerun()

    # ── Journal ──
    elif "Journal" in page:
        st.markdown("<h2 style='color:#e2e8f0'>📔 Mood Journal</h2>", unsafe_allow_html=True)

        # journal_write_count bumps after each save → forces completely fresh widgets
        wc = st.session_state.get("journal_write_count", 0)
        expand_new = st.session_state.get("journal_expand_new", True)

        with st.expander("✏️ Write New Entry", expanded=expand_new):
            j_title = st.text_input("Title", placeholder="Give your entry a title...", key=f"j_title_{wc}")
            j_body  = st.text_area("What's on your mind?", placeholder="Write freely...", height=160, key=f"j_body_{wc}")
            if st.button("💾 Save Entry", use_container_width=True, key=f"save_journal_{wc}"):
                if not j_body.strip():
                    st.warning("Please write something first.")
                else:
                    result  = detect_text_local(j_body)
                    emotion = result["emotion"]
                    meta    = EMOTION_META.get(emotion, EMOTION_META["neutral"])
                    st.session_state.journal.insert(0, {
                        "id":    int(time.time()),
                        "title": j_title.strip() or "Untitled",
                        "body":  j_body,
                        "emotion": emotion,
                        "date":  datetime.now().strftime("%d %b %Y, %H:%M")
                    })
                    # Bump key → clears inputs, collapse expander
                    st.session_state["journal_write_count"] = wc + 1
                    st.session_state["journal_expand_new"]  = False
                    save_user_data()
                    st.success(f"✅ Saved! Detected emotion: {meta['emoji']} **{emotion.title()}**")
                    st.rerun()
            # Button to open a fresh entry
            if not expand_new:
                if st.button("✏️ Write another entry", use_container_width=True, key=f"new_entry_{wc}"):
                    st.session_state["journal_expand_new"] = True
                    st.rerun()

        if not st.session_state.journal:
            st.info("No journal entries yet. Write your first entry above!")
        else:
            for entry in st.session_state.journal:
                emotion = entry.get("emotion","neutral")
                meta    = EMOTION_META.get(emotion, EMOTION_META["neutral"])
                c1,c2 = st.columns([0.9,0.1])
                with c1:
                    st.markdown(f"""
                    <div class="journal-card">
                      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
                        <span style="font-size:1.5rem">{meta['emoji']}</span>
                        <strong style="color:{meta['color']};font-size:1rem">{entry['title']}</strong>
                        <span style="color:#475569;font-size:0.78rem;margin-left:auto">{entry['date']}</span>
                      </div>
                      <div style="color:#cbd5e1;font-size:0.92rem;line-height:1.65">{entry['body'][:280]}{'...' if len(entry['body'])>280 else ''}</div>
                      <div style="margin-top:10px;font-size:0.8rem;color:#64748b">Detected: {meta['emoji']} {emotion.title()}</div>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    if st.button("🗑", key=f"del_{entry['id']}"):
                        st.session_state.journal=[j for j in st.session_state.journal if j["id"]!=entry["id"]]; save_user_data(); st.rerun()

    # ── Assistant ──
    elif "Assistant" in page:

        first_name   = first if first else "there"
        user_initial = first_name[0].upper()

        # Init chat
        if "chat" not in st.session_state or not st.session_state.chat:
            st.session_state.chat = [{
                "role": "assistant",
                "content": f"Hey {first_name}! I am your MoodMate AI companion. I am here to listen, support, and chat with you about anything on your mind. How are you feeling today?"
            }]

        # System prompt
        system_prompt = f"""You are MoodMate AI, a warm and empathetic AI companion.
The user name is {first_name}. Be their safe space to talk about feelings freely.

Rules:
- Always respond with genuine empathy and care
- Give a UNIQUE response every time based on what they said
- 2 to 4 sentences, conversational and warm like a real friend
- Never repeat the same response
- Validate their feelings first then ask a follow up question
- Use their name occasionally
- No bullet points, speak naturally"""

        # Render messages using st.chat_message (native Streamlit — always works)
        for msg in st.session_state.chat:
            if msg["role"] == "assistant":
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("user", avatar="👤"):
                    st.markdown(msg["content"])

        # Clear button below chat
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Clear Conversation", use_container_width=True, key="clr_chat"):
                st.session_state.chat = [{
                    "role": "assistant",
                    "content": f"Fresh start, {first_name}! I am right here whenever you are ready. What is on your mind?"
                }]
                save_user_data()
                st.rerun()

        # Chat input
        user_input = st.chat_input("Type your message here...", key="ai_input")

        if user_input and user_input.strip():
            # Show user message immediately
            st.session_state.chat.append({"role": "user", "content": user_input.strip()})

            # Call Claude API
            with st.spinner("MoodMate AI is typing..."):
                try:
                    msgs_to_send = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.chat
                    ]
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={"Content-Type": "application/json"},
                        json={
                            "model":      "claude-sonnet-4-20250514",
                            "max_tokens": 300,
                            "system":     system_prompt,
                            "messages":   msgs_to_send
                        },
                        timeout=30
                    )
                    if response.ok:
                        reply = response.json()["content"][0]["text"]
                    else:
                        raise Exception(f"API returned {response.status_code}")

                except Exception as e:
                    # Smart fallback based on what user actually said
                    txt = user_input.lower()
                    if any(w in txt for w in ["ignore","ignored","alone","lonely","left out","nobody","no one"]):
                        reply = f"That feeling of being ignored by the people around you really hurts, {first_name}. It makes you feel invisible even in a room full of people. You deserve to be seen and heard. What happened today?"
                    elif any(w in txt for w in ["sad","cry","upset","hurt","pain","broken"]):
                        reply = f"I am so sorry you are feeling this way, {first_name}. Your feelings are completely real and valid. You do not have to pretend everything is okay here. Can you tell me more about what happened?"
                    elif any(w in txt for w in ["friend","friends","class","school","college"]):
                        reply = f"It sounds like something happened with your friends or at school, {first_name}. That can really affect how the whole day feels. I am listening — what is going on?"
                    elif any(w in txt for w in ["happy","good","great","excited","joy"]):
                        reply = f"That is wonderful to hear, {first_name}! It makes me happy knowing you are feeling good. What has been making your day so positive?"
                    elif any(w in txt for w in ["angry","frustrated","mad","annoyed"]):
                        reply = f"I can hear that something is really bothering you, {first_name}. That frustration is completely valid. Tell me what happened and I am here to listen."
                    elif any(w in txt for w in ["anxious","scared","nervous","fear","worry","worried"]):
                        reply = f"Feeling anxious is really hard to deal with alone, {first_name}. But you reached out and that takes courage. Take a slow breath — what has been worrying you?"
                    else:
                        reply = f"Thank you for sharing that with me, {first_name}. I am genuinely here for you and I want to understand what you are going through. Can you tell me a little more so I can be there for you properly?"

            st.session_state.chat.append({"role": "assistant", "content": reply})
            save_user_data()
            st.rerun()


# ── Router ──
pg = st.session_state.page
if   pg=="landing":          show_landing()
elif pg=="login":             show_auth("login")
elif pg=="signup":            show_auth("signup")
elif pg=="app" and st.session_state.user: show_app()
else: st.session_state.page="landing"; st.rerun()
