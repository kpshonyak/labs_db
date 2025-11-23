# routes/customer_routes.py
from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from services.customer_service import CustomerService
from domain.customer import Customer

customer_bp = Blueprint('customers', __name__, url_prefix='/api/customers')

# GET All
@customer_bp.route('/', methods=['GET'])
def get_all_customers():
    service = CustomerService(SessionLocal())
    customers = service.find_all()
    return jsonify([customer.to_dict() for customer in customers]), 200

# GET by ID
@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    service = CustomerService(SessionLocal())
    customer = service.find_by_id(customer_id)
    if customer:
        return jsonify(customer.to_dict()), 200
    return jsonify({'error': 'Customer not found'}), 404

# POST Create
@customer_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    required_fields = ['name', 'surname', 'email']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

    service = CustomerService(SessionLocal())
    if service.find_by_email(data['email']):
        return jsonify({'error': 'Email already exists'}), 400

    new_customer = Customer(
        name=data['name'],
        surname=data['surname'],
        email=data['email'],
        phone=data.get('phone')
    )
    created_customer = service.create(new_customer)
    return jsonify(created_customer.to_dict()), 201

# PUT Update
@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    service = CustomerService(SessionLocal())
    customer = service.find_by_id(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
        
    if 'email' in data and data['email'] != customer.email and service.find_by_email(data['email']):
        return jsonify({'error': 'Email already exists'}), 400
        
    service.update(customer_id, data)
    updated_customer = service.find_by_id(customer_id)
    return jsonify(updated_customer.to_dict()), 200

# DELETE
@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    service = CustomerService(SessionLocal())
    if not service.find_by_id(customer_id):
        return jsonify({'error': 'Customer not found'}), 404
    service.delete(customer_id)
    return jsonify({'message': 'Customer deleted successfully'}), 200

# M:1: Клієнт -> Замовлення
@customer_bp.route('/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    service = CustomerService(SessionLocal())
    if not service.find_by_id(customer_id):
        return jsonify({'error': 'Customer not found'}), 404
    orders = service.find_orders(customer_id)
    return jsonify([order.to_dict() for order in orders]), 200