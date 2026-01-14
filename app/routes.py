from flask import Blueprint, jsonify, request
from app.models import Venue, db
from flask_jwt_extended import jwt_required

main_bp = Blueprint('main', __name__)

# 1. READ ALL (GET)
@main_bp.route('/venues', methods=['GET'])
def get_venues():
    venues = Venue.query.all()
    output = []
    for v in venues:
        output.append({
            'id': v.id,
            'name': v.name,
            'category': v.category,
            'vibe': v.cultural_etiquette
        })
    return jsonify(output), 200

# 2. READ ONE (GET) - Diversification!
@main_bp.route('/venues/<int:id>', methods=['GET'])
def get_single_venue(id):
    venue = Venue.query.get_or_404(id)
    return jsonify({
        'name': venue.name,
        'category': venue.category,
        'vibe': venue.cultural_etiquette
    }), 200

# 3. CREATE (POST) - Secured with JWT
@main_bp.route('/venues', methods=['POST'])
@jwt_required()
def add_venue():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"message": "Missing required data"}), 400
        
    new_v = Venue(
        name=data['name'], 
        category=data.get('category', 'General'), 
        cultural_etiquette=data.get('etiquette', 'Respect local customs')
    )
    db.session.add(new_v)
    db.session.commit()
    return jsonify({"message": "Venue added to Tunis by Night!"}), 201

# 4. UPDATE FULL (PUT) - Diversification!
@main_bp.route('/venues/<int:id>', methods=['PUT'])
@jwt_required()
def update_venue(id):
    venue = Venue.query.get_or_404(id)
    data = request.get_json()
    
    venue.name = data['name']
    venue.category = data['category']
    venue.cultural_etiquette = data['etiquette']
    
    db.session.commit()
    return jsonify({"message": f"Venue {id} fully updated"}), 200

# 5. UPDATE PARTIAL (PATCH) - Diversification!
@main_bp.route('/venues/<int:id>', methods=['PATCH'])
@jwt_required()
def patch_venue(id):
    venue = Venue.query.get_or_404(id)
    data = request.get_json()
    
    if 'etiquette' in data:
        venue.cultural_etiquette = data['etiquette']
    if 'category' in data:
        venue.category = data['category']
        
    db.session.commit()
    return jsonify({"message": f"Venue {id} partially updated"}), 200

# 6. DELETE (DELETE) - Diversification!
@main_bp.route('/venues/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_venue(id):
    venue = Venue.query.get_or_404(id)
    db.session.delete(venue)
    db.session.commit()
    return jsonify({"message": "Venue deleted from collection"}), 200