from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.customer_controller import CustomerController
from domain.customer import Customer

customer_bp = Blueprint('customers', __name__, url_prefix='/api/customers')

@customer_bp.route('/', methods=['GET'])
def get_all_customers():
    controller = CustomerController(SessionLocal())
    customers = controller.find_all()
    return jsonify([c.to_dict() for c in customers]), 200

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    controller = CustomerController(SessionLocal())
    customer = controller.find_by_id(customer_id)
    if customer:
        return jsonify(customer.to_dict()), 200
    return jsonify({'error': 'Customer not found'}), 404

@customer_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    controller = CustomerController(SessionLocal())
    if controller.find_by_email(data['email']):
        return jsonify({'error': 'Email already exists'}), 400

    new_customer = Customer(
        name=data['name'],
        surname=data['surname'],
        email=data['email'],
        phone=data.get('phone')
    )
    created = controller.create(new_customer)
    return jsonify(created.to_dict()), 201

@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    controller = CustomerController(SessionLocal())
    if not controller.find_by_id(customer_id):
        return jsonify({'error': 'Customer not found'}), 404
    controller.update(customer_id, data)
    return jsonify(controller.find_by_id(customer_id).to_dict()), 200

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    controller = CustomerController(SessionLocal())
    if not controller.find_by_id(customer_id):
        return jsonify({'error': 'Customer not found'}), 404
    controller.delete(customer_id)
    return jsonify({'message': 'Customer deleted successfully'}), 200

# M:1
@customer_bp.route('/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    controller = CustomerController(SessionLocal())
    if not controller.find_by_id(customer_id):
        return jsonify({'error': 'Customer not found'}), 404
    orders = controller.find_orders(customer_id)
    return jsonify([o.to_dict() for o in orders]), 200