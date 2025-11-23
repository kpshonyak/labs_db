from dao.base_dao import BaseDAO
from domain.customer import Customer

class CustomerDAO(BaseDAO):
    """
    Data Access Object for Customer entity.
    """
    _model = Customer

    def __init__(self, session):
        self._session = session

    
    def find_by_email(self, email: str):
        """
        Finds a customer by email.
        :param email: email to search
        :return: Customer object or None
        """
        return self._session.query(self._model).filter_by(email=email).first()


    def find_orders(self, customer_id: int):
        """
        Finds all orders placed by a specific customer.
        :param customer_id: Customer ID
        :return: List of Order objects
        """
        from domain.order import Order
        return self._session.query(Order).filter_by(customer_id=customer_id).all()