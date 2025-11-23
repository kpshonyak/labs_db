# services/artist_service.py
from services.base_service import BaseService
from dao.artist_dao import ArtistDAO

class ArtistService(BaseService):
    """Business logic layer for Artist entity."""
    
    def __init__(self, session):
        self._dao = ArtistDAO(session)

    # Логіка для виведення подій артиста (M:M)
    def find_events(self, artist_id: int):
        return self._dao.find_events(artist_id)