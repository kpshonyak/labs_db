from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))

    # Зв'язок 1:M до Orders
    orders = relationship("Order", back_populates="customer")

    def to_dict(self, include_nested=False):
        data = {
            "customer_id": self.customer_id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "phone": self.phone
        }
        if include_nested and hasattr(self, 'orders') and self.orders:
             data['orders'] = [o.to_dict() for o in self.orders]
        return data