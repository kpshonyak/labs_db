# services/customer_service.py
from services.base_service import BaseService
from dao.customer_dao import CustomerDAO

class CustomerService(BaseService):
    """Business logic layer for Customer entity."""
    
    def __init__(self, session):
        self._dao = CustomerDAO(session)

    # Логіка для виведення замовлень клієнта (M:1)
    def find_orders(self, customer_id: int):
        return self._dao.find_orders(customer_id)
        
    # Логіка для перевірки унікальності email
    def find_by_email(self, email: str):
        return self._dao.find_by_email(email)