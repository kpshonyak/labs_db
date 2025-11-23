from dao.base_dao import BaseDAO
from domain.transport_payment import TransportPayment

class TransportPaymentDAO(BaseDAO):
    _model = TransportPayment

    def __init__(self, session):
        self._session = session