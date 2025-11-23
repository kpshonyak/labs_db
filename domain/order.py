from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base

class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    order_date = Column(DateTime, server_default=func.now())
    status = Column(Enum('pending', 'paid', 'cancelled'), default='pending')

    customer = relationship("Customer", back_populates="orders")
    order_tickets = relationship("OrderTicket", back_populates="order")
    payments = relationship("Payment", back_populates="order")

    def to_dict(self, include_nested=False):
        data = {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "status": self.status
        }
        
        if include_nested:
            if hasattr(self, 'customer') and self.customer:
                data['customer'] = self.customer.to_dict()
            if hasattr(self, 'payments') and self.payments:
                # Вивід інформації про оплату
                data['payments'] = [p.to_dict() for p in self.payments]
            if hasattr(self, 'order_tickets') and self.order_tickets:
                # Вивід замовлених квитків
                data['tickets'] = [ot.to_dict() for ot in self.order_tickets]
                
        return data