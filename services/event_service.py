# services/event_service.py
from services.base_service import BaseService
from dao.event_dao import EventDAO

class EventService(BaseService):
    """Business logic layer for Event entity."""
    
    def __init__(self, session):
        self._dao = EventDAO(session)

    # Логіка для виведення артистів події (M:M)
    def find_artists(self, event_id: int):
        return self._dao.find_artists(event_id)
        
    # Логіка для виведення місць події (M:1)
    def find_seats(self, event_id: int):
        return self._dao.find_seats(event_id)