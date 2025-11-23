from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.ticket_controller import TicketController
from domain.ticket import Ticket

ticket_bp = Blueprint('tickets', __name__, url_prefix='/api/tickets')

@ticket_bp.route('/', methods=['GET'])
def get_all_tickets():
    controller = TicketController(SessionLocal())
    tickets = controller.find_all()
    return jsonify([t.to_dict() for t in tickets]), 200

@ticket_bp.route('/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    controller = TicketController(SessionLocal())
    ticket = controller.find_by_id(ticket_id)
    if ticket:
        return jsonify(ticket.to_dict()), 200
    return jsonify({'error': 'Ticket not found'}), 404

@ticket_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.get_json()
    controller = TicketController(SessionLocal())
    new_ticket = Ticket(
        event_id=data['event_id'],
        seat_id=data.get('seat_id'),
        price=data['price']
    )
    created = controller.create(new_ticket)
    return jsonify(created.to_dict()), 201

@ticket_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    data = request.get_json()
    controller = TicketController(SessionLocal())
    if not controller.find_by_id(ticket_id):
        return jsonify({'error': 'Ticket not found'}), 404
    controller.update(ticket_id, data)
    return jsonify(controller.find_by_id(ticket_id).to_dict()), 200

@ticket_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    controller = TicketController(SessionLocal())
    if not controller.find_by_id(ticket_id):
        return jsonify({'error': 'Ticket not found'}), 404
    controller.delete(ticket_id)
    return jsonify({'message': 'Ticket deleted successfully'}), 200

@ticket_bp.route('/event/<int:event_id>', methods=['GET'])
def get_tickets_by_event(event_id):
    controller = TicketController(SessionLocal())
    tickets = controller.find_by_event(event_id)
    return jsonify([t.to_dict() for t in tickets]), 200