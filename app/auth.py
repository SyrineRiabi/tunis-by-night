from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
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
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Credentials required"}), 400

    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        # Using flask-jwt-extended (cleaner & more secure)
        # Identity is usually the user ID or username
        access_token = create_access_token(identity=user.username)
        
        return jsonify({
            "token": access_token, 
            "message": "Login successful",
            "username": user.username
        }), 200
    
    return jsonify({"message": "Invalid credentials"}), 401