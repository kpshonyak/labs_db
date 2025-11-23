from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.payment_controller import PaymentController
from domain.payment import Payment

payment_bp = Blueprint('payments', __name__, url_prefix='/api/payments')

@payment_bp.route('/', methods=['GET'])
def get_all_payments():
    controller = PaymentController(SessionLocal())
    payments = controller.find_all()
    return jsonify([p.to_dict() for p in payments]), 200

@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    controller = PaymentController(SessionLocal())
    payment = controller.find_by_id(payment_id)
    if payment:
        return jsonify(payment.to_dict()), 200
    return jsonify({'error': 'Payment not found'}), 404

@payment_bp.route('/', methods=['POST'])
def create_payment():
    data = request.get_json()
    controller = PaymentController(SessionLocal())
    new_payment = Payment(
        order_id=data['order_id'],
        amount=data['amount'],
        method=data['method']
    )
    created = controller.create(new_payment)
    return jsonify(created.to_dict()), 201

@payment_bp.route('/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    data = request.get_json()
    controller = PaymentController(SessionLocal())
    if not controller.find_by_id(payment_id):
        return jsonify({'error': 'Payment not found'}), 404
    controller.update(payment_id, data)
    return jsonify(controller.find_by_id(payment_id).to_dict()), 200

@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    controller = PaymentController(SessionLocal())
    if not controller.find_by_id(payment_id):
        return jsonify({'error': 'Payment not found'}), 404
    controller.delete(payment_id)
    return jsonify({'message': 'Payment deleted successfully'}), 200

@payment_bp.route('/order/<int:order_id>', methods=['GET'])
def get_payments_by_order(order_id):
    controller = PaymentController(SessionLocal())
    payments = controller.find_by_order(order_id)
    return jsonify([p.to_dict() for p in payments]), 200