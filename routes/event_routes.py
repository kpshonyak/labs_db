from flask import Blueprint, request, jsonify # Не забудьте імпортувати request
from config.db import SessionLocal
from services.event_service import EventService
from domain.event import Event

event_bp = Blueprint('events', __name__, url_prefix='/api/events')

@event_bp.route('/', methods=['GET'])
def get_all_events():
    include_nested = request.args.get('nested', 'false').lower() == 'true'

    service = EventService(SessionLocal())
    events = service.find_all()

    return jsonify([event.to_dict(include_nested=include_nested) for event in events]), 200

@event_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    include_nested = request.args.get('nested', 'false').lower() == 'true'
    
    service = EventService(SessionLocal())
    event = service.find_by_id(event_id)
    
    if event:
        return jsonify(event.to_dict(include_nested=include_nested)), 200
    return jsonify({'error': 'Event not found'}), 404

# POST Create
@event_bp.route('/', methods=['POST'])
def create_event():
    data = request.get_json()
    required_fields = ['title', 'event_date', 'location']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

    service = EventService(SessionLocal())
    new_event = Event(
        title=data['title'],
        event_date=data['event_date'],
        location=data['location']
    )
    created_event = service.create(new_event)
    return jsonify(created_event.to_dict()), 201

# PUT Update
@event_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    service = EventService(SessionLocal())
    if not service.find_by_id(event_id):
        return jsonify({'error': 'Event not found'}), 404
    service.update(event_id, data)
    updated_event = service.find_by_id(event_id)
    return jsonify(updated_event.to_dict()), 200

# DELETE
@event_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    service = EventService(SessionLocal())
    if not service.find_by_id(event_id):
        return jsonify({'error': 'Event not found'}), 404
    service.delete(event_id)
    return jsonify({'message': 'Event deleted successfully'}), 200

# M:M: Подія -> Артисти
@event_bp.route('/<int:event_id>/artists', methods=['GET'])
def get_event_artists(event_id):
    service = EventService(SessionLocal())
    if not service.find_by_id(event_id):
        return jsonify({'error': 'Event not found'}), 404
    artists = service.find_artists(event_id)
    return jsonify([artist.to_dict() for artist in artists]), 200
    
# M:1: Подія -> Місця
@event_bp.route('/<int:event_id>/seats', methods=['GET'])
def get_event_seats(event_id):
    service = EventService(SessionLocal())
    if not service.find_by_id(event_id):
        return jsonify({'error': 'Event not found'}), 404
    seats = service.find_seats(event_id)
    return jsonify([seat.to_dict() for seat in seats]), 200