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


    def find_transport_tickets(self, customer_id: int):
        """
        Знаходить транспортні квитки, придбані клієнтом, пов'язаним із замовленням.
        :param customer_id: Customer ID
        :return: List of TransportTicket objects
        """
     
        from domain.transport_ticket import TransportTicket
        
     
        return self._session.query(TransportTicket).filter_by(customer_id=customer_id).all()