from controllers.base_controller import BaseController
from services.delivery_option_service import DeliveryOptionService

class DeliveryOptionController(BaseController):
    def __init__(self, session):
        super().__init__(DeliveryOptionService(session))