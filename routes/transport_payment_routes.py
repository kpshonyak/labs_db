from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.transport_payment_controller import TransportPaymentController
from domain.transport_payment import TransportPayment

transport_payment_bp = Blueprint('transport_payments', __name__, url_prefix='/api/transport/payments')

@transport_payment_bp.route('/', methods=['GET'])
def get_all_payments():
    controller = TransportPaymentController(SessionLocal())
    payments = controller.find_all()
    return jsonify([p.to_dict() for p in payments]), 200

@transport_payment_bp.route('/<int:t_payment_id>', methods=['GET'])
def get_payment(t_payment_id):
    controller = TransportPaymentController(SessionLocal())
    payment = controller.find_by_id(t_payment_id)
    if payment:
        return jsonify(payment.to_dict()), 200
    return jsonify({'error': 'Payment not found'}), 404

@transport_payment_bp.route('/', methods=['POST'])
def create_payment():
    data = request.get_json()
    controller = TransportPaymentController(SessionLocal())
    new_payment = TransportPayment(
        t_ticket_id=data['t_ticket_id'],
        amount=data['amount'],
        method=data['method']
    )
    created = controller.create(new_payment)
    return jsonify(created.to_dict()), 201

@transport_payment_bp.route('/<int:t_payment_id>', methods=['PUT'])
def update_payment(t_payment_id):
    data = request.get_json()
    controller = TransportPaymentController(SessionLocal())
    if not controller.find_by_id(t_payment_id):
        return jsonify({'error': 'Payment not found'}), 404
    controller.update(t_payment_id, data)
    return jsonify(controller.find_by_id(t_payment_id).to_dict()), 200

@transport_payment_bp.route('/<int:t_payment_id>', methods=['DELETE'])
def delete_payment(t_payment_id):
    controller = TransportPaymentController(SessionLocal())
    if not controller.find_by_id(t_payment_id):
        return jsonify({'error': 'Payment not found'}), 404
    controller.delete(t_payment_id)
    return jsonify({'message': 'Payment deleted successfully'}), 200