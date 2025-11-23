from dao.base_dao import BaseDAO
from domain.transport_ticket import TransportTicket

class TransportTicketDAO(BaseDAO):
    _model = TransportTicket

    def __init__(self, session):
        self._session = session
        
    def find_payments(self, t_ticket_id: int):
        from domain.transport_payment import TransportPayment
        return self._session.query(TransportPayment).filter_by(t_ticket_id=t_ticket_id).all()