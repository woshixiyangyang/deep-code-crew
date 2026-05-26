from abc import ABC, abstractmethod


class StorageService(ABC):
    @abstractmethod
    def load_rooms(self):
        pass

    @abstractmethod
    def save_rooms(self, rooms):
        pass
