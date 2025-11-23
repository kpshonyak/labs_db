from dao.base_dao import BaseDAO
from domain.delivery_option import DeliveryOption

class DeliveryOptionDAO(BaseDAO):
    _model = DeliveryOption

    def __init__(self, session):
        self._session = session