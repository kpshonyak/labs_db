# services/payment_service.py
from services.base_service import BaseService
from dao.payment_dao import PaymentDAO

class PaymentService(BaseService):
    """Business logic layer for Payment entity."""
    
    def __init__(self, session):
        self._dao = PaymentDAO(session)

    # Логіка для знаходження платежів замовлення (M:1)
    def find_by_order(self, order_id: int):
        return self._dao.find_by_order(order_id)