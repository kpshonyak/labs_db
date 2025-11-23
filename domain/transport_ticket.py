from sqlalchemy import Column, Integer, DECIMAL, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class TransportTicket(Base):
    __tablename__ = 'transport_tickets'

    t_ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('transport_routes.route_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    seat_number = Column(String(10))
    price = Column(DECIMAL(10, 2), nullable=False)

    # Зв'язок M:1 до TransportRoute
    route = relationship("TransportRoute", back_populates="transport_tickets")
    payments = relationship("TransportPayment", back_populates="transport_ticket")
    # Зв'язок M:1 до Customer
    customer = relationship("Customer") 

    def to_dict(self):
        return {
            "t_ticket_id": self.t_ticket_id,
            "route_id": self.route_id,
            "customer_id": self.customer_id,
            "seat_number": self.seat_number,
            "price": float(self.price),
        }