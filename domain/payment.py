from sqlalchemy import Column, Integer, Enum, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base

class Payment(Base):
    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_date = Column(DateTime, server_default=func.now())
    method = Column(Enum('card', 'paypal', 'cash', 'bank_transfer'), nullable=False)

    order = relationship("Order", back_populates="payments")

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "order_id": self.order_id,
            "amount": float(self.amount),
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "method": self.method
        }