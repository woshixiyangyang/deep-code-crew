from models.chat_message import ChatMessage
from models.menu_item import MenuItem
from models.room import Room
from .storage_service import StorageService

try:
    import gspread
    from gspread.exceptions import WorksheetNotFound
    from google.oauth2.service_account import Credentials
except ImportError:
    gspread = None
    WorksheetNotFound = None
    Credentials = None

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

ROOM_HEADERS = [
    "room_id",
    "title",
    "host_name",
    "target_people",
    "max_people",
    "order_type",
    "deadline_minutes",
    "meal_time",
    "status",
    "total_price",
    "payment_per_person",
]
MEMBER_HEADERS = ["room_id", "member_name"]
MENU_HEADERS = ["room_id", "menu_id", "menu_name", "price", "quantity"]
CHAT_HEADERS = ["room_id", "user_name", "message", "created_at"]


class GoogleSheetService(StorageService):
    def __init__(self, sheet_id, credentials_path="service_account.json"):
        if gspread is None or Credentials is None:
            raise RuntimeError(
                "GoogleSheetService requires gspread and google-auth."
            )

        creds = Credentials.from_service_account_file(
            credentials_path, scopes=SCOPES
        )
        client = gspread.authorize(creds)
        self.spreadsheet = client.open_by_key(sheet_id)
        self.rooms_ws = self._get_or_create_worksheet("rooms", ROOM_HEADERS)
        self.members_ws = self._get_or_create_worksheet("members", MEMBER_HEADERS)
        self.menu_ws = self._get_or_create_worksheet("menu_items", MENU_HEADERS)
        self.chat_ws = self._get_or_create_worksheet(
            "chat_messages", CHAT_HEADERS
        )

    def load_rooms(self):
        room_rows = self.rooms_ws.get_all_records()
        member_rows = self.members_ws.get_all_records()
        menu_rows = self.menu_ws.get_all_records()
        chat_rows = self.chat_ws.get_all_records()

        rooms = []
        for row in room_rows:
            room_id = self._to_int(row.get("room_id"))
            if room_id <= 0:
                continue

            members = [
                str(member.get("member_name", ""))
                for member in member_rows
                if self._to_int(member.get("room_id")) == room_id
                and str(member.get("member_name", "")).strip()
            ]

            menu_items = [
                MenuItem(
                    item_id=self._to_int(menu.get("menu_id")),
                    name=str(menu.get("menu_name", "")),
                    price=self._to_int(menu.get("price")),
                    quantity=max(self._to_int(menu.get("quantity")), 1),
                )
                for menu in menu_rows
                if self._to_int(menu.get("room_id")) == room_id
            ]

            chat_messages = [
                ChatMessage(
                    sender_name=str(chat.get("user_name", "")),
                    message=str(chat.get("message", "")),
                    created_at=str(chat.get("created_at", "")),
                )
                for chat in chat_rows
                if self._to_int(chat.get("room_id")) == room_id
            ]

            target_people = max(self._to_int(row.get("target_people")), 1)
            max_people = self._to_int(row.get("max_people"), target_people)
            if max_people < target_people:
                max_people = target_people

            rooms.append(
                Room(
                    room_id=room_id,
                    title=str(row.get("title", "")),
                    host_name=str(row.get("host_name", "")),
                    target_people=target_people,
                    max_people=max_people,
                    order_type=str(row.get("order_type", "")),
                    deadline_minutes=self._to_int(row.get("deadline_minutes")),
                    meal_time=str(row.get("meal_time", "")),
                    status=str(row.get("status", "")) or "모집중",
                    members=members,
                    menu_items=menu_items,
                    chat_messages=chat_messages,
                )
            )

        return rooms

    def save_rooms(self, rooms):
        room_rows = []
        member_rows = []
        menu_rows = []
        chat_rows = []

        for room in rooms:
            room_rows.append(
                [
                    room.room_id,
                    room.title,
                    room.host_name,
                    room.target_people,
                    room.max_people,
                    room.order_type,
                    room.deadline_minutes,
                    room.meal_time,
                    room.status,
                    room.total_price(),
                    room.split_payment(),
                ]
            )

            for member in room.members:
                member_rows.append([room.room_id, member])

            for item in room.menu_items:
                menu_rows.append(
                    [
                        room.room_id,
                        item.item_id,
                        item.name,
                        item.price,
                        item.quantity,
                    ]
                )

            for chat in room.chat_messages:
                chat_rows.append(
                    [
                        room.room_id,
                        chat.sender_name,
                        chat.message,
                        chat.created_at,
                    ]
                )

        self._replace_rows(self.rooms_ws, ROOM_HEADERS, room_rows)
        self._replace_rows(self.members_ws, MEMBER_HEADERS, member_rows)
        self._replace_rows(self.menu_ws, MENU_HEADERS, menu_rows)
        self._replace_rows(self.chat_ws, CHAT_HEADERS, chat_rows)

    def _get_or_create_worksheet(self, title, headers):
        try:
            worksheet = self.spreadsheet.worksheet(title)
        except WorksheetNotFound:
            worksheet = self.spreadsheet.add_worksheet(
                title=title,
                rows=100,
                cols=max(len(headers), 1),
            )

        current_headers = worksheet.row_values(1)
        if current_headers != headers:
            worksheet.update([headers], "A1")
        return worksheet

    def _replace_rows(self, worksheet, headers, rows):
        required_rows = max(len(rows) + 1, 1000)
        required_cols = max(len(headers), worksheet.col_count)
        worksheet.resize(rows=required_rows, cols=required_cols)
        worksheet.clear()
        worksheet.update([headers], "A1")
        if rows:
            worksheet.update(rows, "A2")

    def _to_int(self, value, default=0):
        if value in ("", None):
            return default
        try:
            return int(value)
        except (TypeError, ValueError):
            return default
