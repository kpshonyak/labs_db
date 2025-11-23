from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.artist_controller import ArtistController
from domain.artist import Artist

artist_bp = Blueprint('artists', __name__, url_prefix='/api/artists')

@artist_bp.route('/', methods=['GET'])
def get_all_artists():
    controller = ArtistController(SessionLocal())
    artists = controller.find_all()
    return jsonify([artist.to_dict() for artist in artists]), 200

@artist_bp.route('/<int:artist_id>', methods=['GET'])
def get_artist(artist_id):
    controller = ArtistController(SessionLocal())
    artist = controller.find_by_id(artist_id)
    if artist:
        return jsonify(artist.to_dict()), 200
    return jsonify({'error': 'Artist not found'}), 404

@artist_bp.route('/', methods=['POST'])
def create_artist():
    data = request.get_json()
    if not data or 'full_name' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    controller = ArtistController(SessionLocal())
    new_artist = Artist(
        full_name=data['full_name'],
        stage_name=data.get('stage_name'),
        genre=data.get('genre'),
        country=data.get('country')
    )
    created = controller.create(new_artist)
    return jsonify(created.to_dict()), 201

@artist_bp.route('/<int:artist_id>', methods=['PUT'])
def update_artist(artist_id):
    data = request.get_json()
    controller = ArtistController(SessionLocal())
    if not controller.find_by_id(artist_id):
        return jsonify({'error': 'Artist not found'}), 404
    controller.update(artist_id, data)
    return jsonify(controller.find_by_id(artist_id).to_dict()), 200

@artist_bp.route('/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    controller = ArtistController(SessionLocal())
    if not controller.find_by_id(artist_id):
        return jsonify({'error': 'Artist not found'}), 404
    controller.delete(artist_id)
    return jsonify({'message': 'Artist deleted successfully'}), 200

# M:M
@artist_bp.route('/<int:artist_id>/events', methods=['GET'])
def get_artist_events(artist_id):
    controller = ArtistController(SessionLocal())
    if not controller.find_by_id(artist_id):
        return jsonify({'error': 'Artist not found'}), 404
    events = controller.find_events(artist_id)
    return jsonify([event.to_dict() for event in events]), 200