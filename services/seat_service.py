from services.base_service import BaseService
from dao.seat_dao import SeatDAO

class SeatService(BaseService):
    """Business logic layer for Seat entity."""
    
    def __init__(self, session):
        self._dao = SeatDAO(session)

    # Логіка для знаходження доступних місць
    def find_available(self, event_id: int):
        return self._dao.find_available(event_id)