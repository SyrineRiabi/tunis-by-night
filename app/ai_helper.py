import os
import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/chat', methods=['POST'])
def chat():
    """
    AI Chatbot Endpoint
    ---
    tags:
      - AI Services
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            prompt:
              type: string
              example: "Where should I go for coffee in Sidi Bou Said?"
    responses:
      200:
        description: AI reply received successfully
      400:
        description: Google rejected the payload
    """
    data = request.json or {}
    user_message = data.get("prompt") or data.get("message")
    
    if not user_message:
        return jsonify({"reply": "Empty message received"}), 400

    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": user_message}]}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        res_data = response.json()

        if response.status_code == 200:
            ai_reply = res_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"reply": ai_reply, "status": "success"})
        else:
            print(f"GOOGLE ERROR REASON: {res_data}")
            return jsonify({
                "reply": "Google rejection.",
                "debug": res_data.get('error', {}).get('message', 'Check API Key/Region')
            }), 400

    except Exception as e:
        return jsonify({"reply": "Backend Connection Error", "error": str(e)}), 500