# routes/delivery_option_routes.py
from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from services.delivery_option_service import DeliveryOptionService
from domain.delivery_option import DeliveryOption

delivery_option_bp = Blueprint('delivery_options', __name__, url_prefix='/api/delivery')

# GET All
@delivery_option_bp.route('/', methods=['GET'])
def get_all_delivery_options():
    service = DeliveryOptionService(SessionLocal())
    options = service.find_all()
    return jsonify([option.to_dict() for option in options]), 200

# GET by ID
@delivery_option_bp.route('/<int:delivery_id>', methods=['GET'])
def get_delivery_option(delivery_id):
    service = DeliveryOptionService(SessionLocal())
    option = service.find_by_id(delivery_id)
    if option:
        return jsonify(option.to_dict()), 200
    return jsonify({'error': 'Delivery option not found'}), 404

# POST Create
@delivery_option_bp.route('/', methods=['POST'])
def create_delivery_option():
    data = request.get_json()
    required_fields = ['method']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

    service = DeliveryOptionService(SessionLocal())
    new_option = DeliveryOption(
        method=data['method'],
        price=data.get('price')
    )
    created_option = service.create(new_option)
    return jsonify(created_option.to_dict()), 201

# PUT Update
@delivery_option_bp.route('/<int:delivery_id>', methods=['PUT'])
def update_delivery_option(delivery_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    service = DeliveryOptionService(SessionLocal())
    if not service.find_by_id(delivery_id):
        return jsonify({'error': 'Delivery option not found'}), 404
    service.update(delivery_id, data)
    updated_option = service.find_by_id(delivery_id)
    return jsonify(updated_option.to_dict()), 200

# DELETE
@delivery_option_bp.route('/<int:delivery_id>', methods=['DELETE'])
def delete_delivery_option(delivery_id):
    service = DeliveryOptionService(SessionLocal())
    if not service.find_by_id(delivery_id):
        return jsonify({'error': 'Delivery option not found'}), 404
    service.delete(delivery_id)
    return jsonify({'message': 'Delivery option deleted successfully'}), 200