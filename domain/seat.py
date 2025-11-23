from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from config.db import Base

class Seat(Base):
    __tablename__ = 'seats'
    
    seat_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.event_id'), nullable=False)
    seat_number = Column(String(10), nullable=False)
    section = Column(String(50))
    is_available = Column(Boolean, default=True)

    event = relationship("Event", back_populates="seats")
    ticket = relationship("Ticket", back_populates="seat", uselist=False)

    def to_dict(self):
        return {
            "seat_id": self.seat_id,
            "event_id": self.event_id,
            "seat_number": self.seat_number,
            "section": self.section,
            "is_available": self.is_available
        }