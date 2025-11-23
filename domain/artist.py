# domain/artist.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base
from domain.association_tables import ArtistEventAssociation

class Artist(Base):
    __tablename__ = 'artists'

    artist_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(150), nullable=False)
    stage_name = Column(String(150), unique=True)
    genre = Column(String(50))
    country = Column(String(50))

    # Зв'язок
    events = relationship("Event", secondary=ArtistEventAssociation, back_populates="artists")

    # Цей метод важливий для вкладеного вигляду
    def to_dict(self):
        return {
            "artist_id": self.artist_id,
            "name": self.full_name,     # У вашому JSON прикладі це 'name'
            "bio": self.genre,          # Приклад мапінгу
            "stage_name": self.stage_name,
            "country": self.country
        }