import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    
    # FIX: Your JS sends "prompt", but code was looking for "message"
    # We check both to be safe!
    user_message = data.get("prompt") or data.get("message")
    
    if not user_message:
        return jsonify({"reply": "Error: No message received from frontend"}), 400

    api_key = os.getenv("GOOGLE_API_KEY")
    # v1beta is the safest for AI Studio keys right now
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # Simplified payload structure
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        res_data = response.json()

        if response.status_code == 200:
            ai_reply = res_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_reply, "status": "success"})
        else:
            print(f"DEBUG GOOGLE ERROR: {res_data}")
            return jsonify({
                "reply": f"Google Error {response.status_code}",
                "details": res_data.get('error', {}).get('message', 'Bad Request')
            }), 400

    except Exception as e:
        return jsonify({"reply": "Backend error", "error": str(e)}), 500