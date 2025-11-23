from controllers.base_controller import BaseController
from services.seat_service import SeatService

class SeatController(BaseController):
    def __init__(self, session):
        super().__init__(SeatService(session))
        
    def find_available(self, event_id: int):
        return self._service.find_available(event_id)