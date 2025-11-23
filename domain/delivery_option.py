from sqlalchemy import Column, Integer, Enum, DECIMAL
from config.db import Base

class DeliveryOption(Base):
    __tablename__ = 'delivery_options'

    delivery_id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(Enum('email', 'pickup', 'courier'), nullable=False, unique=True)
    price = Column(DECIMAL(6, 2), default='0.00')

    def to_dict(self):
        return {
            "delivery_id": self.delivery_id,
            "method": self.method,
            "price": float(self.price)
        }