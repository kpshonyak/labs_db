import os
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv
from config.db import SessionLocal
from routes.artist_routes import artist_bp
import domain
from routes.event_routes import event_bp
from routes.customer_routes import customer_bp
from routes.order_routes import order_bp
from routes.ticket_routes import ticket_bp
from routes.seat_routes import seat_bp
from routes.payment_routes import payment_bp
from routes.transport_route_routes import transport_route_bp
from routes.transport_ticket_routes import transport_ticket_bp
from routes.transport_payment_routes import transport_payment_bp
from routes.delivery_option_routes import delivery_option_bp
from routes.order_ticket_routes import order_ticket_bp
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    app.register_blueprint(artist_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(seat_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(transport_route_bp)
    app.register_blueprint(transport_ticket_bp)
    app.register_blueprint(transport_payment_bp)
    app.register_blueprint(delivery_option_bp)
    app.register_blueprint(order_ticket_bp)

    @app.teardown_appcontext
    def remove_session(exception=None):
        SessionLocal.remove()

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        SessionLocal.remove()
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
        SessionLocal.remove()
        return jsonify({'error': str(error)}), 500

    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to Event Ticketing API',
        'version': '1.0',
        'endpoints': {
            'artists': {
                'GET /api/artists': 'Get all artists',
                'GET /api/artists/<id>': 'Get artist by ID (CRUD)',
                'POST /api/artists': 'Create a new artist (CRUD)',
                'GET /api/artists/<id>/events': 'Get all events for a specific artist (M:M relation)'
            },
            'events': {
                'GET /api/events': 'Get all events',
                'GET /api/events/<id>': 'Get event by ID (CRUD)',
                'POST /api/events': 'Create a new event (CRUD)',
                'GET /api/events/<id>/artists': 'Get all artists for an event (M:M relation)',
                'GET /api/events/<id>/seats': 'Get all seats for an event (M:1 relation)'
            },
            'customers': {
                'GET /api/customers': 'Get all customers',
                'GET /api/customers/<id>': 'Get customer by ID (CRUD)',
                'POST /api/customers': 'Create a new customer (CRUD)',
                'GET /api/customers/<id>/orders': 'Get all orders placed by a customer (M:1 relation)'
            },
            'orders': {
                'GET /api/orders': 'Get all orders',
                'GET /api/orders/<id>': 'Get order by ID (CRUD)',
                'POST /api/orders': 'Create a new order (CRUD)',
                'GET /api/orders/<id>/tickets': 'Get all event tickets in an order (M:M relation)',
                'GET /api/orders/<id>/transport': 'Get transport tickets linked to the customer (M:1 relation)'
            },
            'tickets': {
                'GET /api/tickets': 'Get all event tickets',
                'GET /api/tickets/<id>': 'Get ticket by ID (CRUD)',
                'POST /api/tickets': 'Create a new ticket (CRUD)',
                'GET /api/tickets/event/<id>': 'Get tickets filtered by event ID'
            },
            'seats': {
                'GET /api/seats': 'Get all seats',
                'GET /api/seats/available/<id>': 'Get all available seats for an event',
                'GET /api/seats/<id>': 'Get seat by ID (CRUD)',
                'POST /api/seats': 'Create a new seat (CRUD)'
            },
            'payments': {
                'GET /api/payments': 'Get all order payments',
                'GET /api/payments/<id>': 'Get payment by ID (CRUD)',
                'POST /api/payments': 'Create a new payment (CRUD)',
                'GET /api/payments/order/<id>': 'Get all payments for a specific order (M:1 relation)'
            },
            'transport_routes': {
                'GET /api/transport/routes': 'Get all transport routes (CRUD)',
                'POST /api/transport/routes': 'Create a new route',
                'GET /api/transport/routes/<id>/tickets': 'Get all transport tickets for a route (M:1 relation)'
            },
            'transport_tickets': {
                'GET /api/transport/tickets': 'Get all transport tickets (CRUD)',
                'POST /api/transport/tickets': 'Create a new transport ticket',
                'GET /api/transport/tickets/<id>/payments': 'Get payments for a transport ticket (M:1 relation)'
            },
            'delivery_options': {
                'GET /api/delivery': 'Get all delivery options (CRUD)',
                'POST /api/delivery': 'Create a new option'
            },
            'order_tickets': {
                'GET /api/order-tickets': 'Get all order-ticket M:M links (CRUD)'
                }
            }
        }), 200

    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200

    return app


if __name__ == '__main__':
    app = create_app()
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', '5000'))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    logger.info(f"Starting Flask application on http://{host}:{port}")
    app.run(debug=debug, host=host, port=port)
