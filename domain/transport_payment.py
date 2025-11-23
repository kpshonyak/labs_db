from sqlalchemy import Column, Integer, DECIMAL, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base

class TransportPayment(Base):
    __tablename__ = 'transport_payments'

    t_payment_id = Column(Integer, primary_key=True, autoincrement=True)
    t_ticket_id = Column(Integer, ForeignKey('transport_tickets.t_ticket_id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_date = Column(DateTime, server_default=func.now())
    method = Column(Enum('card', 'paypal', 'cash'), nullable=False)

    transport_ticket = relationship("TransportTicket", back_populates="payments")

    def to_dict(self):
        return {
            "t_payment_id": self.t_payment_id,
            "t_ticket_id": self.t_ticket_id,
            "amount": float(self.amount),
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "method": self.method
        }