from controllers.base_controller import BaseController
from services.order_ticket_service import OrderTicketService

class OrderTicketController(BaseController):
    def __init__(self, session):
        super().__init__(OrderTicketService(session))
        
    def find_by_ticket_id(self, ticket_id: int):
        return self._service.find_by_ticket_id(ticket_id)