from dao.base_dao import BaseDAO
from domain.order_ticket import OrderTicket

class OrderTicketDAO(BaseDAO):
    _model = OrderTicket

    def __init__(self, session):
        self._session = session
        
    def find_by_ticket_id(self, ticket_id: int):
        return self._session.query(self._model).filter_by(ticket_id=ticket_id).first()