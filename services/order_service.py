from services.base_service import BaseService
from dao.order_dao import OrderDAO

class OrderService(BaseService):
    """Business logic layer for Order entity."""
    
    def __init__(self, session):
        self._dao = OrderDAO(session)

    # Логіка для виведення квитків у замовленні (M:M)
    def find_tickets(self, order_id: int):
        return self._dao.find_tickets(order_id)
        
    # Логіка для виведення транспортних квитків
    def find_transport_tickets(self, order_id: int):
        order = self.find_by_id(order_id)
        if not order:
            return []
        return self._dao.find_transport_tickets(order.customer_id)