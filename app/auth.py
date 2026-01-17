from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User Registration
    ---
    tags: [Authentication]
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            username: {type: string, example: "Syrine_Riabi"}
            email: {type: string, example: "syrine@tunis.com"}
            password: {type: string, example: "securePass123"}
    responses:
      201:
        description: User registered successfully
      400:
        description: Missing fields or user already exists
    """
    data = request.get_json()
    
    # Validation: Ensure all fields are present
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing required fields"}), 400

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already taken"}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already registered"}), 400
    
    try:
        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password']) # This uses Bcrypt to hash
        
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User Login
    ---
    tags: [Authentication]
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            username: {type: string, example: "Syrine_Riabi"}
            password: {type: string, example: "securePass123"}
    responses:
      200:
        description: Returns a JWT Access Token
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Credentials required"}), 400

    user = User.query.filter_by(username=data['username']).first()
    
    # Check password using the method in your User model
    if user and user.check_password(data['password']):
        # Create token with identity
        access_token = create_access_token(identity=user.username)
        
        return jsonify({
            "token": access_token, 
            "message": "Login successful",
            "username": user.username
        }), 200
    
    return jsonify({"message": "Invalid credentials"}), 401