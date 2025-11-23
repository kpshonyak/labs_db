from controllers.base_controller import BaseController
from services.artist_service import ArtistService

class ArtistController(BaseController):
    def __init__(self, session):
        super().__init__(ArtistService(session))

    def find_events(self, artist_id: int):
        return self._service.find_events(artist_id)