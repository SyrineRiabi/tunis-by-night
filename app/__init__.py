from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tunis_by_night.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev_key_for_final'

    db.init_app(app)
    bcrypt.init_app(app)

    # Import Blueprints
    from app.routes import main_bp
    from app.auth import auth_bp
    from app.ai_helper import ai_bp # <--- NEW
    
    # Register Blueprints
    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(ai_bp, url_prefix='/api/ai') # <--- NEW

    with app.app_context():
        db.create_all()

    return app