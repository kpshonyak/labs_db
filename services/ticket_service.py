# services/ticket_service.py
from services.base_service import BaseService
from dao.ticket_dao import TicketDAO

class TicketService(BaseService):
    """Business logic layer for Ticket entity."""
    
    def __init__(self, session):
        self._dao = TicketDAO(session)

    # Логіка для знаходження квитків за подією (M:1)
    def find_by_event(self, event_id: int):
        return self._dao.find_by_event(event_id)