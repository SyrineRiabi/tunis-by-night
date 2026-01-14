from flask import Blueprint, jsonify, request
from .models import Venue, db
from flask_jwt_extended import jwt_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/venues', methods=['GET'])
def get_venues():
    venues = Venue.query.all()
    output = []
    for v in venues:
        output.append({
            'name': v.name,
            'category': v.category,
            'vibe': v.cultural_etiquette
        })
    return jsonify(output)

@main_bp.route('/venues', methods=['POST'])
@jwt_required() # Only logged-in users can add new spots!
def add_venue():
    data = request.get_json()
    new_v = Venue(
        name=data['name'], 
        category=data['category'], 
        cultural_etiquette=data['etiquette']
    )
    db.session.add(new_v)
    db.session.commit()
    return jsonify({"message": "Venue added to Tunis by Night!"}), 201