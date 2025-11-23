from dao.base_dao import BaseDAO
from domain.artist import Artist

class ArtistDAO(BaseDAO):
    _model = Artist

    def __init__(self, session):
        self._session = session

    def find_events(self, artist_id: int):
        from domain.event import Event
        from domain.association_tables import ArtistEventAssociation
        
    
        return self._session.query(Event).join(
            ArtistEventAssociation, 
            Event.event_id == ArtistEventAssociation.c.events_event_id
        ).filter(
            ArtistEventAssociation.c.artists_artist_id == artist_id
        ).all()