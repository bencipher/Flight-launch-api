from abc import ABC, abstractmethod


class BaseRepository(ABC):

    def __init__(self, session):
        self.session = session

    @abstractmethod
    def add(self, items):
        pass

    @abstractmethod
    def get(self, id_):
        pass

    @abstractmethod
    def list(self, limit=None, **filters):
        pass

    @abstractmethod
    def update(self, id_, **payload):
        pass

    @abstractmethod
    def delete(self, id_):
        pass
