from sqlalchemy.orm import joinedload 
from dao.base_dao import BaseDAO
from domain.event import Event

class EventDAO(BaseDAO):
    _model = Event

    def __init__(self, session):
        self._session = session

    # Перевизначаємо метод find_all, щоб він вантажив і артистів одразу
    def find_all(self):
        # options(joinedload(Event.artists)) каже: "Дістань події І одразу приєднай артистів"
        return self._session.query(Event).options(joinedload(Event.artists)).all()

    # Те саме для find_by_id
    def find_by_id(self, event_id: int):
        return self._session.query(Event).options(joinedload(Event.artists)).filter_by(event_id=event_id).first()
    # Функція для виведення артистів події (Завдання M:M: вивести для кожного суб’єкта з одної таблиці усі суб’єкти другої таблиці)
    def find_artists(self, event_id: int):
        """
        Finds all artists associated with a specific event using the M:M join table.
        """
        from domain.artist import Artist
        # 1. ЗМІНА ІМПОРТУ
        from domain.association_tables import ArtistEventAssociation

        # 2. ЗМІНА ЗАПИТУ (використовуємо .c для доступу до колонок)
        return self._session.query(Artist).join(
            ArtistEventAssociation, 
            Artist.artist_id == ArtistEventAssociation.c.artists_artist_id
        ).filter(
            ArtistEventAssociation.c.events_event_id == event_id
        ).all()

    # Функція для виведення всіх місць події (Завдання M:1: вивести людей, які в ньому проживають)
    def find_seats(self, event_id: int):
        """
        Finds all seats available for a specific event.
        :param event_id: Event ID
        :return: List of Seat objects
        """
        from domain.seat import Seat
        return self._session.query(Seat).filter_by(event_id=event_id).all()