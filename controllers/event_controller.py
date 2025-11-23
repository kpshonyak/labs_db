from controllers.base_controller import BaseController
from services.event_service import EventService

class EventController(BaseController):
    def __init__(self, session):
        super().__init__(EventService(session))

    def find_artists(self, event_id: int):
        return self._service.find_artists(event_id)

    def find_seats(self, event_id: int):
        return self._service.find_seats(event_id)