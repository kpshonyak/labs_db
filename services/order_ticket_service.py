from services.base_service import BaseService
from dao.order_ticket_dao import OrderTicketDAO

class OrderTicketService(BaseService):
    """Business logic layer for OrderTicket entity."""
    
    def __init__(self, session):
        self._dao = OrderTicketDAO(session)
        
    def find_by_ticket_id(self, ticket_id: int):
        return self._dao.find_by_ticket_id(ticket_id)