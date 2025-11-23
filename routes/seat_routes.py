from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.seat_controller import SeatController
from domain.seat import Seat

seat_bp = Blueprint('seats', __name__, url_prefix='/api/seats')

@seat_bp.route('/', methods=['GET'])
def get_all_seats():
    controller = SeatController(SessionLocal())
    seats = controller.find_all()
    return jsonify([s.to_dict() for s in seats]), 200

@seat_bp.route('/<int:seat_id>', methods=['GET'])
def get_seat(seat_id):
    controller = SeatController(SessionLocal())
    seat = controller.find_by_id(seat_id)
    if seat:
        return jsonify(seat.to_dict()), 200
    return jsonify({'error': 'Seat not found'}), 404

@seat_bp.route('/', methods=['POST'])
def create_seat():
    data = request.get_json()
    controller = SeatController(SessionLocal())
    new_seat = Seat(
        event_id=data['event_id'],
        seat_number=data['seat_number'],
        section=data.get('section'),
        is_available=data.get('is_available', True)
    )
    created = controller.create(new_seat)
    return jsonify(created.to_dict()), 201

@seat_bp.route('/<int:seat_id>', methods=['PUT'])
def update_seat(seat_id):
    data = request.get_json()
    controller = SeatController(SessionLocal())
    if not controller.find_by_id(seat_id):
        return jsonify({'error': 'Seat not found'}), 404
    controller.update(seat_id, data)
    return jsonify(controller.find_by_id(seat_id).to_dict()), 200

@seat_bp.route('/<int:seat_id>', methods=['DELETE'])
def delete_seat(seat_id):
    controller = SeatController(SessionLocal())
    if not controller.find_by_id(seat_id):
        return jsonify({'error': 'Seat not found'}), 404
    controller.delete(seat_id)
    return jsonify({'message': 'Seat deleted successfully'}), 200

@seat_bp.route('/available/<int:event_id>', methods=['GET'])
def get_available_seats(event_id):
    controller = SeatController(SessionLocal())
    seats = controller.find_available(event_id)
    return jsonify([s.to_dict() for s in seats]), 200