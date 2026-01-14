from flask import Blueprint, request, jsonify

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').lower()
    
    # Simple logic for tonight's demo
    if "sidi bou said" in user_message:
        response = "Sidi Bou Said is perfect for a night walk! I recommend Cafe des Delices for the view."
    elif "club" in user_message or "dance" in user_message:
        response = "For dancing, you should check out Gammarth. Don't miss 'The Fridge' or 'Yuka'!"
    else:
        response = "I'm your Tunis Night Expert. Ask me about cafes, clubs, or the best views in the city!"

    return jsonify({
        "status": "success",
        "reply": response
    })