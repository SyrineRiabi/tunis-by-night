import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flasgger import Swagger

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

    # Swagger Configuration
    app.config['SWAGGER'] = {
        'title': 'Tunis By Night API',
        'uiversion': 3
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Tunis By Night API",
            "description": "Interactive API documentation for the 2026 Nightlife Guide",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Add 'Bearer <your_token>'"
            }
        }
    }

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    Swagger(app, template=swagger_template)

    # Import Blueprints
    from app.routes import main_bp
    from app.auth import auth_bp
    from app.ai_helper import ai_bp
    
    # REGISTER BLUEPRINTS
    app.register_blueprint(main_bp, url_prefix='/api') 
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(ai_bp, url_prefix='/api')

    @app.route('/')
    def root():
        from flask import render_template
        return render_template('index.html')

    with app.app_context():
        db.create_all()

    return app 