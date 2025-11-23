from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.event_controller import EventController
from domain.event import Event

event_bp = Blueprint('events', __name__, url_prefix='/api/events')

@event_bp.route('/', methods=['GET'])
def get_all_events():
    include_nested = request.args.get('nested', 'false').lower() == 'true'
    controller = EventController(SessionLocal())
    events = controller.find_all()
    return jsonify([event.to_dict(include_nested=include_nested) for event in events]), 200

@event_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    include_nested = request.args.get('nested', 'false').lower() == 'true'
    controller = EventController(SessionLocal())
    event = controller.find_by_id(event_id)
    if event:
        return jsonify(event.to_dict(include_nested=include_nested)), 200
    return jsonify({'error': 'Event not found'}), 404

@event_bp.route('/', methods=['POST'])
def create_event():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    controller = EventController(SessionLocal())
    new_event = Event(
        title=data['title'],
        event_date=data['event_date'],
        location=data['location']
    )
    created = controller.create(new_event)
    return jsonify(created.to_dict()), 201

@event_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    controller = EventController(SessionLocal())
    if not controller.find_by_id(event_id):
        return jsonify({'error': 'Event not found'}), 404
    controller.update(event_id, data)
    return jsonify(controller.find_by_id(event_id).to_dict()), 200

@event_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    controller = EventController(SessionLocal())
    if not controller.find_by_id(event_id):
        return jsonify({'error': 'Event not found'}), 404
    controller.delete(event_id)
    return jsonify({'message': 'Event deleted successfully'}), 200

# M:M
@event_bp.route('/<int:event_id>/artists', methods=['GET'])
def get_event_artists(event_id):
    controller = EventController(SessionLocal())
    if not controller.find_by_id(event_id):
        return jsonify({'error': 'Event not found'}), 404
    artists = controller.find_artists(event_id)
    return jsonify([a.to_dict() for a in artists]), 200

# M:1
@event_bp.route('/<int:event_id>/seats', methods=['GET'])
def get_event_seats(event_id):
    controller = EventController(SessionLocal())
    if not controller.find_by_id(event_id):
        return jsonify({'error': 'Event not found'}), 404
    seats = controller.find_seats(event_id)
    return jsonify([s.to_dict() for s in seats]), 200