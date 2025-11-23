from dao.base_dao import BaseDAO
from domain.seat import Seat

class SeatDAO(BaseDAO):
    _model = Seat

    def __init__(self, session):
        self._session = session
        
    def find_available(self, event_id: int):
        return self._session.query(self._model).filter_by(event_id=event_id, is_available=True).all()