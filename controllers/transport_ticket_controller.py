from controllers.base_controller import BaseController
from services.transport_ticket_service import TransportTicketService

class TransportTicketController(BaseController):
    def __init__(self, session):
        super().__init__(TransportTicketService(session))
        
    def find_payments(self, t_ticket_id: int):
        return self._service.find_payments(t_ticket_id)