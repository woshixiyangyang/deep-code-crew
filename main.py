import os
import sys

from controllers.party_controller import PartyController
from services.google_sheet_service import GoogleSheetService
from services.local_storage_service import LocalStorageService
from views.console_view import ConsoleView

# A identity: YING LAN / 2023106179 / A - Controller and core Model structure


def main():
    storage_service = create_storage_service()
    view = ConsoleView()
    controller = PartyController(view, storage_service)
    controller.run()


def create_storage_service():
    sheet_id = os.environ.get("GOOGLE_SHEET_ID", "").strip()
    credentials_path = os.environ.get("GOOGLE_CREDENTIALS_PATH", "").strip()

    if sheet_id and credentials_path:
        if not os.path.exists(credentials_path):
            print("[Storage] Google Sheets mode")
            print(f"[Error] Credential file not found: {credentials_path}")
            sys.exit(1)
        try:
            print("[Storage] Google Sheets mode")
            return GoogleSheetService(sheet_id, credentials_path)
        except Exception as error:
            print(f"[Error] Google Sheets storage failed: {error}")
            sys.exit(1)

    print("[Storage] LocalStorage mode")
    return LocalStorageService("local_storage.json")


if __name__ == "__main__":
    main()
