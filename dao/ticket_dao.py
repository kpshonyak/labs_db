from dao.base_dao import BaseDAO
from domain.ticket import Ticket

class TicketDAO(BaseDAO):
    _model = Ticket

    def __init__(self, session):
        self._session = session
        
    def find_by_event(self, event_id: int):
        return self._session.query(self._model).filter_by(event_id=event_id).all()