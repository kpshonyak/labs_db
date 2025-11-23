from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.order_ticket_controller import OrderTicketController
from domain.order_ticket import OrderTicket

order_ticket_bp = Blueprint('order_tickets', __name__, url_prefix='/api/order-tickets')

@order_ticket_bp.route('/', methods=['GET'])
def get_all_items():
    controller = OrderTicketController(SessionLocal())
    items = controller.find_all()
    return jsonify([item.to_dict() for item in items]), 200

@order_ticket_bp.route('/<int:id>', methods=['GET'])
def get_item(id):
    controller = OrderTicketController(SessionLocal())
    item = controller.find_by_id(id)
    if item:
        return jsonify(item.to_dict()), 200
    return jsonify({'error': 'Item not found'}), 404

@order_ticket_bp.route('/', methods=['POST'])
def create_item():
    data = request.get_json()
    controller = OrderTicketController(SessionLocal())
    new_item = OrderTicket(
        order_id=data['order_id'],
        ticket_id=data['ticket_id'],
        delivery_id=data.get('delivery_id')
    )
    created = controller.create(new_item)
    return jsonify(created.to_dict()), 201

@order_ticket_bp.route('/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    controller = OrderTicketController(SessionLocal())
    if not controller.find_by_id(id):
        return jsonify({'error': 'Item not found'}), 404
    controller.update(id, data)
    return jsonify(controller.find_by_id(id).to_dict()), 200

@order_ticket_bp.route('/<int:id>', methods=['DELETE'])
def delete_item(id):
    controller = OrderTicketController(SessionLocal())
    if not controller.find_by_id(id):
        return jsonify({'error': 'Item not found'}), 404
    controller.delete(id)
    return jsonify({'message': 'Item deleted successfully'}), 200