from dao.base_dao import BaseDAO
from domain.payment import Payment

class PaymentDAO(BaseDAO):
    _model = Payment

    def __init__(self, session):
        self._session = session
        
    def find_by_order(self, order_id: int):
        return self._session.query(self._model).filter_by(order_id=order_id).all()