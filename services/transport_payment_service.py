# services/transport_payment_service.py
from services.base_service import BaseService
from dao.transport_payment_dao import TransportPaymentDAO

class TransportPaymentService(BaseService):
    """Business logic layer for TransportPayment entity."""
    
    def __init__(self, session):
        self._dao = TransportPaymentDAO(session)