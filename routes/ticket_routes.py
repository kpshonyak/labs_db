# routes/ticket_routes.py
from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from services.ticket_service import TicketService
from domain.ticket import Ticket

ticket_bp = Blueprint('tickets', __name__, url_prefix='/api/tickets')

# GET All
@ticket_bp.route('/', methods=['GET'])
def get_all_tickets():
    service = TicketService(SessionLocal())
    tickets = service.find_all()
    return jsonify([ticket.to_dict() for ticket in tickets]), 200

# GET by ID
@ticket_bp.route('/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    service = TicketService(SessionLocal())
    ticket = service.find_by_id(ticket_id)
    if ticket:
        return jsonify(ticket.to_dict()), 200
    return jsonify({'error': 'Ticket not found'}), 404

# POST Create
@ticket_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.get_json()
    required_fields = ['event_id', 'price']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400

    service = TicketService(SessionLocal())
    new_ticket = Ticket(
        event_id=data['event_id'],
        seat_id=data.get('seat_id'),
        price=data['price']
    )
    created_ticket = service.create(new_ticket)
    return jsonify(created_ticket.to_dict()), 201

# PUT Update
@ticket_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    service = TicketService(SessionLocal())
    if not service.find_by_id(ticket_id):
        return jsonify({'error': 'Ticket not found'}), 404
    service.update(ticket_id, data)
    updated_ticket = service.find_by_id(ticket_id)
    return jsonify(updated_ticket.to_dict()), 200

# DELETE
@ticket_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    service = TicketService(SessionLocal())
    if not service.find_by_id(ticket_id):
        return jsonify({'error': 'Ticket not found'}), 404
    service.delete(ticket_id)
    return jsonify({'message': 'Ticket deleted successfully'}), 200

# M:1: Отримати квитки за подією
@ticket_bp.route('/event/<int:event_id>', methods=['GET'])
def get_tickets_by_event(event_id):
    service = TicketService(SessionLocal())
    tickets = service.find_by_event(event_id)
    return jsonify([ticket.to_dict() for ticket in tickets]), 200