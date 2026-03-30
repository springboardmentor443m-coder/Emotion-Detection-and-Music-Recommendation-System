import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load env variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key="AIzaSyDUbruxkR2yeZNAFOsKBrZa08mnl7nafmc" 
)

# -------------------------------
# STEP 1: Mood Detection Prompt
# -------------------------------
MOOD_PROMPT = """
You are an emotion detection AI.

Analyze the user's message and classify it into EXACTLY one of these emotions:
Angry, Fear, Happy, Sad, Surprise, Neutral

Rules:
- Only output ONE word from the list
- Do not explain anything
- Do not add punctuation

Examples:
"I feel amazing today!" → Happy
"I am scared about tomorrow" → Fear
"I hate everything" → Angry
"""

# -------------------------------
# STEP 2: Response Generator Prompt
# -------------------------------
RESPONSE_PROMPT = """
You are a supportive AI assistant.

The user's mood is: {mood}

Respond appropriately:
- Angry → calm and de-escalate
- Fear → reassure and comfort
- Happy → celebrate and uplift
- Sad → empathize and support
- Surprise → respond with curiosity/excitement
- Neutral → be friendly and engaging

Keep response:
- Under 120 words
- Warm and human-like
- No robotic tone
"""

# -------------------------------
# API Route
# -------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message")

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # -------------------------------
        # STEP 1: Detect Mood
        # -------------------------------
        mood_messages = [
            SystemMessage(content=MOOD_PROMPT),
            HumanMessage(content=user_input)
        ]

        mood_response = llm.invoke(mood_messages)
        detected_mood = mood_response.content.strip()

        # Safety fallback
        allowed_moods = ["Angry", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
        if detected_mood not in allowed_moods:
            detected_mood = "Neutral"

        # -------------------------------
        # STEP 2: Generate Response
        # -------------------------------
        final_prompt = RESPONSE_PROMPT.format(mood=detected_mood)

        response_messages = [
            SystemMessage(content=final_prompt),
            HumanMessage(content=user_input)
        ]

        final_response = llm.invoke(response_messages)

        return jsonify({
            "mood": detected_mood,
            "reply": final_response.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5050)