# domain/event.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from config.db import Base
from domain.association_tables import ArtistEventAssociation

class Event(Base):
    __tablename__ = 'events'

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    event_date = Column(DateTime, nullable=False)
    location = Column(String(100), nullable=False, index=True)

    # Зв'язки
    artists = relationship("Artist", secondary=ArtistEventAssociation, back_populates="events")
    seats = relationship("Seat", back_populates="event")
    tickets = relationship("Ticket", back_populates="event")

    # --- ОНОВЛЕНИЙ МЕТОД to_dict З УМОВОЮ ---
    def to_dict(self, include_nested=False):
        # 1. Створюємо базовий словник (тільки дані події)
        data = {
            "event_id": self.event_id,
            "title": self.title,
            "event_date": self.event_date.isoformat() if self.event_date else None,
            "location": self.location
        }

        # 2. Якщо попросили вкладені дані - додаємо їх
        if include_nested:
            # Перевіряємо, чи є артисти, щоб не викликати помилку
            if self.artists:
                data['artists'] = [artist.to_dict() for artist in self.artists]
            else:
                data['artists'] = []

        return data