from controllers.base_controller import BaseController
from services.order_service import OrderService

class OrderController(BaseController):
    def __init__(self, session):
        super().__init__(OrderService(session))

    def find_tickets(self, order_id: int):
        return self._service.find_tickets(order_id)

    def find_transport_tickets(self, order_id: int):
        return self._service.find_transport_tickets(order_id)