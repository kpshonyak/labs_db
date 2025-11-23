from controllers.base_controller import BaseController
from services.transport_payment_service import TransportPaymentService

class TransportPaymentController(BaseController):
    def __init__(self, session):
        super().__init__(TransportPaymentService(session))