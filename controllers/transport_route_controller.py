from controllers.base_controller import BaseController
from services.transport_route_service import TransportRouteService

class TransportRouteController(BaseController):
    def __init__(self, session):
        super().__init__(TransportRouteService(session))
        
    def find_tickets(self, route_id: int):
        return self._service.find_tickets(route_id)