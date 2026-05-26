from controllers.party_controller import PartyController
from services.local_storage_service import LocalStorageService
from views.console_view import ConsoleView

# A identity: YING LAN / 2023106179 / A - Controller and core Model structure


def main():
    storage_service = LocalStorageService("local_storage.json")
    view = ConsoleView()
    controller = PartyController(view, storage_service)
    controller.run()


if __name__ == "__main__":
    main()
