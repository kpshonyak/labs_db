from controllers.base_controller import BaseController
from services.customer_service import CustomerService

class CustomerController(BaseController):
    def __init__(self, session):
        super().__init__(CustomerService(session))

    def find_orders(self, customer_id: int):
        return self._service.find_orders(customer_id)
        
    def find_by_email(self, email: str):
        return self._service.find_by_email(email)