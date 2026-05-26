from .storage_service import StorageService


class GoogleSheetService(StorageService):
    def load_rooms(self):
        # TODO(B): Load room rows, menu rows, and chat rows from Google Sheets.
        # This placeholder keeps local development runnable without credentials.
        return []

    def save_rooms(self, rooms):
        # TODO(B): Save rooms, members, menu items, and chat messages to Google Sheets.
        # This placeholder intentionally does nothing until credentials are added.
        pass
