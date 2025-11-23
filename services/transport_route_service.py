# services/transport_route_service.py
from services.base_service import BaseService
from dao.transport_route_dao import TransportRouteDAO

class TransportRouteService(BaseService):
    """Business logic layer for TransportRoute entity."""
    
    def __init__(self, session):
        self._dao = TransportRouteDAO(session)

    # Логіка для знаходження квитків маршруту (M:1)
    def find_tickets(self, route_id: int):
        return self._dao.find_tickets(route_id)