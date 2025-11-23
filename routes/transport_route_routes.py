from flask import Blueprint, request, jsonify
from config.db import SessionLocal
from controllers.transport_route_controller import TransportRouteController
from domain.transport_route import TransportRoute

transport_route_bp = Blueprint('transport_routes', __name__, url_prefix='/api/transport/routes')

@transport_route_bp.route('/', methods=['GET'])
def get_all_routes():
    controller = TransportRouteController(SessionLocal())
    routes = controller.find_all()
    return jsonify([r.to_dict() for r in routes]), 200

@transport_route_bp.route('/<int:route_id>', methods=['GET'])
def get_route(route_id):
    controller = TransportRouteController(SessionLocal())
    route = controller.find_by_id(route_id)
    if route:
        return jsonify(route.to_dict()), 200
    return jsonify({'error': 'Route not found'}), 404

@transport_route_bp.route('/', methods=['POST'])
def create_route():
    data = request.get_json()
    controller = TransportRouteController(SessionLocal())
    new_route = TransportRoute(
        type=data['type'],
        origin=data['origin'],
        destination=data['destination'],
        departure=data['departure'],
        arrival=data['arrival']
    )
    created = controller.create(new_route)
    return jsonify(created.to_dict()), 201

@transport_route_bp.route('/<int:route_id>', methods=['PUT'])
def update_route(route_id):
    data = request.get_json()
    controller = TransportRouteController(SessionLocal())
    if not controller.find_by_id(route_id):
        return jsonify({'error': 'Route not found'}), 404
    controller.update(route_id, data)
    return jsonify(controller.find_by_id(route_id).to_dict()), 200

@transport_route_bp.route('/<int:route_id>', methods=['DELETE'])
def delete_route(route_id):
    controller = TransportRouteController(SessionLocal())
    if not controller.find_by_id(route_id):
        return jsonify({'error': 'Route not found'}), 404
    controller.delete(route_id)
    return jsonify({'message': 'Route deleted successfully'}), 200

@transport_route_bp.route('/<int:route_id>/tickets', methods=['GET'])
def get_route_tickets(route_id):
    controller = TransportRouteController(SessionLocal())
    tickets = controller.find_tickets(route_id)
    return jsonify([t.to_dict() for t in tickets]), 200