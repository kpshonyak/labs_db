from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.delivery_option_controller import DeliveryOptionController
from domain.delivery_option import DeliveryOption

delivery_option_bp = Blueprint('delivery_options', __name__, url_prefix='/api/delivery')

@delivery_option_bp.route('/', methods=['GET'])
def get_all_options():
    controller = DeliveryOptionController(SessionLocal())
    options = controller.find_all()
    return jsonify([o.to_dict() for o in options]), 200

@delivery_option_bp.route('/<int:delivery_id>', methods=['GET'])
def get_option(delivery_id):
    controller = DeliveryOptionController(SessionLocal())
    option = controller.find_by_id(delivery_id)
    if option:
        return jsonify(option.to_dict()), 200
    return jsonify({'error': 'Option not found'}), 404

@delivery_option_bp.route('/', methods=['POST'])
def create_option():
    data = request.get_json()
    controller = DeliveryOptionController(SessionLocal())
    new_option = DeliveryOption(
        method=data['method'],
        price=data.get('price')
    )
    created = controller.create(new_option)
    return jsonify(created.to_dict()), 201

@delivery_option_bp.route('/<int:delivery_id>', methods=['PUT'])
def update_option(delivery_id):
    data = request.get_json()
    controller = DeliveryOptionController(SessionLocal())
    if not controller.find_by_id(delivery_id):
        return jsonify({'error': 'Option not found'}), 404
    controller.update(delivery_id, data)
    return jsonify(controller.find_by_id(delivery_id).to_dict()), 200

@delivery_option_bp.route('/<int:delivery_id>', methods=['DELETE'])
def delete_option(delivery_id):
    controller = DeliveryOptionController(SessionLocal())
    if not controller.find_by_id(delivery_id):
        return jsonify({'error': 'Option not found'}), 404
    controller.delete(delivery_id)
    return jsonify({'message': 'Option deleted successfully'}), 200