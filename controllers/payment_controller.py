from controllers.base_controller import BaseController
from services.payment_service import PaymentService

class PaymentController(BaseController):
    def __init__(self, session):
        super().__init__(PaymentService(session))
        
    def find_by_order(self, order_id: int):
        return self._service.find_by_order(order_id)