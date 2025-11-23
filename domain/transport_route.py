from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from config.db import Base

class TransportRoute(Base):
    __tablename__ = 'transport_routes'

    transport_tickets = relationship("TransportTicket", back_populates="route")

    route_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum('train', 'flight', 'bus'), nullable=False)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    departure = Column(DateTime, nullable=False)
    arrival = Column(DateTime, nullable=False)

    def to_dict(self):
        return {
            "route_id": self.route_id,
            "type": self.type,
            "origin": self.origin,
            "destination": self.destination,
            "departure": self.departure.isoformat(),
            "arrival": self.arrival.isoformat()
        }