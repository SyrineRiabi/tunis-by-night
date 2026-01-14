from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

# Basic Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tunis_test.db'
app.config['JWT_SECRET_KEY'] = 'tunis-secret'
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database Model
class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    etiquette = db.Column(db.Text)

# Create the DB
with app.app_context():
    db.create_all()

# Routes
@app.route('/api/marhaba', methods=['GET'])
def welcome():
    return jsonify({"message": "Welcome to Tunis by Night!"})

@app.route('/api/login', methods=['POST'])
def login():
    # Simple login for testing
    token = create_access_token(identity="admin")
    return jsonify(access_token=token)

@app.route('/api/venues', methods=['POST'])
@jwt_required()
def add_venue():
    data = request.get_json()
    new_v = Venue(name=data['name'], etiquette=data['etiquette'])
    db.session.add(new_v)
    db.session.commit()
    return jsonify({"message": "Success!"})

if __name__ == '__main__':
    app.run(debug=True)