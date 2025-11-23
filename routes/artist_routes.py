# routes/artist_routes.py
from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from services.artist_service import ArtistService
from domain.artist import Artist

artist_bp = Blueprint('artists', __name__, url_prefix='/api/artists')

# GET All
@artist_bp.route('/', methods=['GET'])
def get_all_artists():
    service = ArtistService(SessionLocal())
    artists = service.find_all()
    return jsonify([artist.to_dict() for artist in artists]), 200

# GET by ID
@artist_bp.route('/<int:artist_id>', methods=['GET'])
def get_artist(artist_id):
    service = ArtistService(SessionLocal())
    artist = service.find_by_id(artist_id)
    if artist:
        return jsonify(artist.to_dict()), 200
    return jsonify({'error': 'Artist not found'}), 404

# POST Create
@artist_bp.route('/', methods=['POST'])
def create_artist():
    data = request.get_json()
    required_fields = ['full_name']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

    service = ArtistService(SessionLocal())
    new_artist = Artist(
        full_name=data['full_name'],
        stage_name=data.get('stage_name'),
        genre=data.get('genre'),
        country=data.get('country')
    )
    created_artist = service.create(new_artist)
    return jsonify(created_artist.to_dict()), 201

# PUT Update
@artist_bp.route('/<int:artist_id>', methods=['PUT'])
def update_artist(artist_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    service = ArtistService(SessionLocal())
    artist = service.find_by_id(artist_id)
    if not artist:
        return jsonify({'error': 'Artist not found'}), 404
    service.update(artist_id, data)
    updated_artist = service.find_by_id(artist_id)
    return jsonify(updated_artist.to_dict()), 200

# DELETE
@artist_bp.route('/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    service = ArtistService(SessionLocal())
    if not service.find_by_id(artist_id):
        return jsonify({'error': 'Artist not found'}), 404
    service.delete(artist_id)
    return jsonify({'message': 'Artist deleted successfully'}), 200

# M:M: Артист -> Події
@artist_bp.route('/<int:artist_id>/events', methods=['GET'])
def get_artist_events(artist_id):
    service = ArtistService(SessionLocal())
    if not service.find_by_id(artist_id):
        return jsonify({'error': 'Artist not found'}), 404
    events = service.find_events(artist_id)
    return jsonify([event.to_dict() for event in events]), 200