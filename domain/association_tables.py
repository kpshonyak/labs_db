
from sqlalchemy import Table, Column, Integer, ForeignKey
from config.db import Base

ArtistEventAssociation = Table(
    'artists_has_events', Base.metadata, # Назва таблиці в MySQL
    Column('artists_artist_id', Integer, ForeignKey('artists.artist_id'), primary_key=True),
    Column('events_event_id', Integer, ForeignKey('events.event_id'), primary_key=True)
)
    