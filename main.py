from controllers.party_controller import PartyController
from services.google_sheet_service import GoogleSheetService
from views.console_view import ConsoleView

# A identity: YING LAN / 2023106179 / A - Controller and core Model structure


def main():
    storage_service = GoogleSheetService("final project")
    view = ConsoleView()
    controller = PartyController(view, storage_service)
    controller.run()


if __name__ == "__main__":
    main()
