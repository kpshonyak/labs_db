from controllers.base_controller import BaseController
from services.ticket_service import TicketService

class TicketController(BaseController):
    def __init__(self, session):
        super().__init__(TicketService(session))
        
    def find_by_event(self, event_id: int):
        return self._service.find_by_event(event_id)