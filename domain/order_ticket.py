from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class OrderTicket(Base):
    """Таблиця зв'язку Order-Ticket-Delivery"""
    __tablename__ = 'order_tickets'
    
    order_ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    ticket_id = Column(Integer, ForeignKey('tickets.ticket_id'), unique=True, nullable=False)
    delivery_id = Column(Integer, ForeignKey('delivery_options.delivery_id'))

 
    order = relationship("Order", back_populates="order_tickets")
    ticket = relationship("Ticket", back_populates="order_link")
    delivery_option = relationship("DeliveryOption")

    def to_dict(self):
        return {
            "order_ticket_id": self.order_ticket_id,
            "order_id": self.order_id,
            "ticket_id": self.ticket_id,
            "delivery_id": self.delivery_id,
            "delivery_method": self.delivery_option.method if self.delivery_option else None,
            "price": self.ticket.price if self.ticket else None
        }