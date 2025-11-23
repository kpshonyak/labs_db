from services.base_service import BaseService
from dao.transport_ticket_dao import TransportTicketDAO

class TransportTicketService(BaseService):
    """Business logic layer for TransportTicket entity."""
    
    def __init__(self, session):
        self._dao = TransportTicketDAO(session)

    # Логіка для знаходження платежів транспортного квитка (M:1)
    def find_payments(self, t_ticket_id: int):
        return self._dao.find_payments(t_ticket_id)