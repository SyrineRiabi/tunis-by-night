import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_message = data.get("message", "Hello")
    
    # Ensure the key is a clean string with no hidden spaces
    api_key = str(os.getenv("GOOGLE_API_KEY")).strip()

    # The most compatible endpoint for AI Studio keys
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    
    # This specific structure is the only one Google accepts without 400 errors
    payload = {
        "contents": [{
            "parts": [{"text": user_message}]
        }]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        res_data = response.json()

        if response.status_code == 200:
            ai_reply = res_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_reply, "status": "success"})
        else:
            # Look at your Docker terminal/logs for this specific output
            print(f"--- API REJECTION ---")
            print(f"Status: {response.status_code}")
            print(f"Response: {res_data}")
            return jsonify({
                "reply": f"Google Error {response.status_code}",
                "debug_info": res_data.get('error', {}).get('message', 'Check logs')
            }), 400

    except Exception as e:
        return jsonify({"reply": "Internal connection failure", "error": str(e)}), 500