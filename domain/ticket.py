from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Ticket(Base):
    __tablename__ = 'tickets'
    
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.event_id'), nullable=False)
    seat_id = Column(Integer, ForeignKey('seats.seat_id'), unique=True)
    price = Column(DECIMAL(10, 2), nullable=False)

    event = relationship("Event", back_populates="tickets")
    seat = relationship("Seat", back_populates="ticket")
    order_link = relationship("OrderTicket", back_populates="ticket", uselist=False)

    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "event_id": self.event_id,
            "seat_id": self.seat_id,
            "price": float(self.price),
            "seat_number": self.seat.seat_number if self.seat else None
        }