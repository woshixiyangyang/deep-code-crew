import json
from pathlib import Path

from models.room import Room

from .storage_service import StorageService


class LocalStorageService(StorageService):
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def _load_data(self):
        if not self.file_path.exists():
            return self._empty_data()

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            return self._empty_data()

        if not isinstance(data, dict):
            return self._empty_data()

        loaded_data = self._empty_data()
        loaded_data.update(data)
        return loaded_data

    def _save_data(self, data):
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def _empty_data(self):
        return {
            "rooms": [],
        }

    def load_rooms(self):
        data = self._load_data()
        return [Room.from_dict(room_data) for room_data in data.get("rooms", [])]

    def save_rooms(self, rooms):
        data = self._load_data()
        data["rooms"] = [room.to_dict() for room in rooms]
        data.pop("user_name", None)
        self._save_data(data)
