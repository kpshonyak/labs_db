from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.transport_ticket_controller import TransportTicketController
from domain.transport_ticket import TransportTicket

transport_ticket_bp = Blueprint('transport_tickets', __name__, url_prefix='/api/transport/tickets')

@transport_ticket_bp.route('/', methods=['GET'])
def get_all_tickets():
    controller = TransportTicketController(SessionLocal())
    tickets = controller.find_all()
    return jsonify([t.to_dict() for t in tickets]), 200

@transport_ticket_bp.route('/<int:t_ticket_id>', methods=['GET'])
def get_ticket(t_ticket_id):
    controller = TransportTicketController(SessionLocal())
    ticket = controller.find_by_id(t_ticket_id)
    if ticket:
        return jsonify(ticket.to_dict()), 200
    return jsonify({'error': 'Ticket not found'}), 404

@transport_ticket_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.get_json()
    controller = TransportTicketController(SessionLocal())
    new_ticket = TransportTicket(
        route_id=data['route_id'],
        customer_id=data['customer_id'],
        price=data['price']
    )
    created = controller.create(new_ticket)
    return jsonify(created.to_dict()), 201

@transport_ticket_bp.route('/<int:t_ticket_id>', methods=['PUT'])
def update_ticket(t_ticket_id):
    data = request.get_json()
    controller = TransportTicketController(SessionLocal())
    if not controller.find_by_id(t_ticket_id):
        return jsonify({'error': 'Ticket not found'}), 404
    controller.update(t_ticket_id, data)
    return jsonify(controller.find_by_id(t_ticket_id).to_dict()), 200

@transport_ticket_bp.route('/<int:t_ticket_id>', methods=['DELETE'])
def delete_ticket(t_ticket_id):
    controller = TransportTicketController(SessionLocal())
    if not controller.find_by_id(t_ticket_id):
        return jsonify({'error': 'Ticket not found'}), 404
    controller.delete(t_ticket_id)
    return jsonify({'message': 'Ticket deleted successfully'}), 200

@transport_ticket_bp.route('/<int:t_ticket_id>/payments', methods=['GET'])
def get_ticket_payments(t_ticket_id):
    controller = TransportTicketController(SessionLocal())
    payments = controller.find_payments(t_ticket_id)
    return jsonify([p.to_dict() for p in payments]), 200