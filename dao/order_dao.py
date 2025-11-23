# dao/order_dao.py
from dao.base_dao import BaseDAO
from domain.order import Order


class OrderDAO(BaseDAO):
    """
    Data Access Object for Order entity.
    Наслідує BaseDAO для базових CRUD-операцій.
    """
    _model = Order

    def __init__(self, session):
        self._session = session

    # Функція для виведення квитків у замовленні (через стикувальну таблицю order_tickets) - Завдання M:M
    def find_tickets(self, order_id: int):
        """
        Знаходить усі квитки на події, включені у конкретне замовлення.
        Використовує JOIN для зв'язку Order -> OrderTicket -> Ticket.
        :param order_id: Order ID
        :return: List of Ticket objects
        """
        # Локальні імпорти, щоб уникнути зациклення
        from domain.ticket import Ticket
        from domain.order_ticket import OrderTicket
        
        return self._session.query(Ticket).join(
            OrderTicket, Ticket.ticket_id == OrderTicket.ticket_id
        ).filter(OrderTicket.order_id == order_id).all()

    # Функція для виведення транспортних квитків (через зв'язок Customer) - Завдання M:1
    def find_transport_tickets(self, customer_id: int):
        """
        Знаходить транспортні квитки, придбані клієнтом, пов'язаним із замовленням.
        :param customer_id: Customer ID
        :return: List of TransportTicket objects
        """
        # Локальний імпорт
        from domain.transport_ticket import TransportTicket
        
        # У вашій схемі TransportTicket має прямий FK до customers.customer_id
        return self._session.query(TransportTicket).filter_by(customer_id=customer_id).all()