from typing import List

class BaseController:
    """
    Base Controller that handles standard CRUD operations by delegating to a Service.
    """
    def __init__(self, service):
        self._service = service

    def find_all(self) -> List[object]:
        return self._service.find_all()

    def find_by_id(self, key: int) -> object:
        return self._service.find_by_id(key)

    def create(self, obj: object) -> object:
        return self._service.create(obj)

    def update(self, key: int, attrs: dict):
        self._service.update(key, attrs)

    def delete(self, key: int):
        self._service.delete(key)
