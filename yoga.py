import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini 2.5 Flash Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY
)

# System prompt 
SYSTEM_PROMPT = """
You are a calm, supportive AI yoga assistant.

Based on the user's emotional state or query, suggest exactly 6 yoga postures.

For each posture:
- Provide the posture name (English + Sanskrit if possible)
- Give 2–3 short benefits
- Keep explanations concise
- Make suggestions practical and beginner-friendly

Format the response clearly like this:

1. Posture Name (Sanskrit Name)
   - Benefit 1
   - Benefit 2
   - Benefit 3

Keep total response under 250 words.
Do not include extra commentary before or after the list.
Be warm and supportive in tone.
Only send the yoga postures not any other comment. Donot give comments like Here are 6 yoga postures that might offer some comfort and gentle uplift
simple give the yoga poses.
"""

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message")

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Create conversation messages
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_input)
        ]

        # Get response from Gemini
        response = llm.invoke(messages)

        return jsonify({
            "reply": response.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)