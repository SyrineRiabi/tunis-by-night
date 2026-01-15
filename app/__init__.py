import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    # Absolute path fix for Docker
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/tunis_by_night.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev_key_for_final'
    app.config['JWT_SECRET_KEY'] = 'tunis_night_secret_2026'

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import Blueprints
    from app.routes import main_bp
    from app.auth import auth_bp
    from app.ai_helper import ai_bp
    
    # REGISTER BLUEPRINTS - Fixed prefixes to match your JS
    app.register_blueprint(main_bp, url_prefix='/api') 
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    # Changed this from /api/ai to /api so it matches your fetch('/api/chat')
    app.register_blueprint(ai_bp, url_prefix='/api')

    @app.route('/')
    def root():
        from flask import render_template
        return render_template('index.html')

    with app.app_context():
        db.create_all()

    return app