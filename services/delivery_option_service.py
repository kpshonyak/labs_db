from services.base_service import BaseService
from dao.delivery_option_dao import DeliveryOptionDAO

class DeliveryOptionService(BaseService):
    """Business logic layer for DeliveryOption entity."""
    
    def __init__(self, session):
        self._dao = DeliveryOptionDAO(session)