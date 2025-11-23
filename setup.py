"""
Setup script to initialize the database and create tables.
Run this script before starting the application.
"""
from config.db import Base, engine

from domain.artist import Artist
from domain.event import Event
from domain.customer import Customer
from domain.order import Order
from domain.ticket import Ticket
from domain.seat import Seat
from domain.transport_route import TransportRoute
from domain.transport_ticket import TransportTicket
from domain.delivery_option import DeliveryOption
from domain.payment import Payment 

def setup_database():
    """
    Creates all database tables based on the defined models.
    """
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

    # List all created tables
    print("\nCreated tables:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")


if __name__ == '__main__':
    setup_database()