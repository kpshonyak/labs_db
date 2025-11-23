from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.order_controller import OrderController
from domain.order import Order

order_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@order_bp.route('/', methods=['GET'])
def get_all_orders():
    controller = OrderController(SessionLocal())
    orders = controller.find_all()
    return jsonify([o.to_dict() for o in orders]), 200

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    controller = OrderController(SessionLocal())
    order = controller.find_by_id(order_id)
    if order:
        return jsonify(order.to_dict()), 200
    return jsonify({'error': 'Order not found'}), 404

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or 'customer_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    controller = OrderController(SessionLocal())
    new_order = Order(
        customer_id=data['customer_id'],
        status=data.get('status', 'pending')
    )
    created = controller.create(new_order)
    return jsonify(created.to_dict()), 201

@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    controller = OrderController(SessionLocal())
    if not controller.find_by_id(order_id):
        return jsonify({'error': 'Order not found'}), 404
    controller.update(order_id, data)
    return jsonify(controller.find_by_id(order_id).to_dict()), 200

@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    controller = OrderController(SessionLocal())
    if not controller.find_by_id(order_id):
        return jsonify({'error': 'Order not found'}), 404
    controller.delete(order_id)
    return jsonify({'message': 'Order deleted successfully'}), 200

# M:M
@order_bp.route('/<int:order_id>/tickets', methods=['GET'])
def get_order_tickets(order_id):
    controller = OrderController(SessionLocal())
    if not controller.find_by_id(order_id):
        return jsonify({'error': 'Order not found'}), 404
    tickets = controller.find_tickets(order_id)
    return jsonify([t.to_dict() for t in tickets]), 200

# M:1
@order_bp.route('/<int:order_id>/transport', methods=['GET'])
def get_order_transport_tickets(order_id):
    controller = OrderController(SessionLocal())
    if not controller.find_by_id(order_id):
        return jsonify({'error': 'Order not found'}), 404
    tickets = controller.find_transport_tickets(order_id)
    return jsonify([t.to_dict() for t in tickets]), 200