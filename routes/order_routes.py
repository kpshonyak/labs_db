# routes/order_routes.py
from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from services.order_service import OrderService
from domain.order import Order

order_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

# GET All
@order_bp.route('/', methods=['GET'])
def get_all_orders():
    service = OrderService(SessionLocal())
    orders = service.find_all()
    return jsonify([order.to_dict() for order in orders]), 200

# GET by ID
@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    service = OrderService(SessionLocal())
    order = service.find_by_id(order_id)
    if order:
        return jsonify(order.to_dict()), 200
    return jsonify({'error': 'Order not found'}), 404

# POST Create
@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    required_fields = ['customer_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

    service = OrderService(SessionLocal())
    new_order = Order(
        customer_id=data['customer_id'],
        status=data.get('status')
    )
    created_order = service.create(new_order)
    return jsonify(created_order.to_dict()), 201

# PUT Update
@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    service = OrderService(SessionLocal())
    if not service.find_by_id(order_id):
        return jsonify({'error': 'Order not found'}), 404
    service.update(order_id, data)
    updated_order = service.find_by_id(order_id)
    return jsonify(updated_order.to_dict()), 200

# DELETE
@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    service = OrderService(SessionLocal())
    if not service.find_by_id(order_id):
        return jsonify({'error': 'Order not found'}), 404
    service.delete(order_id)
    return jsonify({'message': 'Order deleted successfully'}), 200

# M:M: Замовлення -> Квитки на події
@order_bp.route('/<int:order_id>/tickets', methods=['GET'])
def get_order_tickets(order_id):
    service = OrderService(SessionLocal())
    if not service.find_by_id(order_id):
        return jsonify({'error': 'Order not found'}), 404
    tickets = service.find_tickets(order_id)
    return jsonify([ticket.to_dict() for ticket in tickets]), 200

# M:1: Замовлення -> Транспортні квитки
@order_bp.route('/<int:order_id>/transport', methods=['GET'])
def get_order_transport_tickets(order_id):
    service = OrderService(SessionLocal())
    order = service.find_by_id(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    transport_tickets = service.find_transport_tickets(order_id)
    return jsonify([t_ticket.to_dict() for t_ticket in transport_tickets]), 200