from flask import Blueprint, jsonify, request, render_template
from app.models import Venue, db
from flask_jwt_extended import jwt_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/venues', methods=['GET'])
def get_venues():
    """
    List all Nightlife Venues
    ---
    tags:
      - Venue Management
    responses:
      200:
        description: A list of all clubs, bars, and cafes
    """
    venues = Venue.query.all()
    output = [{'id': v.id, 'name': v.name, 'category': v.category, 'vibe': v.cultural_etiquette} for v in venues]
    return jsonify(output), 200

@main_bp.route('/venues/<int:id>', methods=['GET'])
def get_single_venue(id):
    """
    Get Details of a Specific Venue
    ---
    tags:
      - Venue Management
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Venue details
    """
    venue = Venue.query.get_or_404(id)
    return jsonify({'name': venue.name, 'category': venue.category, 'vibe': venue.cultural_etiquette}), 200

@main_bp.route('/venues', methods=['POST'])
@jwt_required()
def add_venue():
    """
    Add a New Venue (Protected)
    ---
    tags:
      - Venue Management
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            name:
              type: string
            category:
              type: string
            etiquette:
              type: string
    responses:
      201:
        description: Venue created
    """
    data = request.get_json()
    new_v = Venue(name=data['name'], category=data.get('category', 'General'), cultural_etiquette=data.get('etiquette', 'Respect local customs'))
    db.session.add(new_v)
    db.session.commit()
    return jsonify({"message": "Venue added!"}), 201

@main_bp.route('/venues/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_venue(id):
    """
    Remove a Venue (Protected)
    ---
    tags:
      - Venue Management
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Venue deleted
    """
    venue = Venue.query.get_or_404(id)
    db.session.delete(venue)
    db.session.commit()
    return jsonify({"message": "Venue deleted"}), 200