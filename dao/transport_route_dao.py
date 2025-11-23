from dao.base_dao import BaseDAO
from domain.transport_route import TransportRoute

class TransportRouteDAO(BaseDAO):
    _model = TransportRoute

    def __init__(self, session):
        self._session = session
        
    def find_tickets(self, route_id: int):
        from domain.transport_ticket import TransportTicket
        return self._session.query(TransportTicket).filter_by(route_id=route_id).all()