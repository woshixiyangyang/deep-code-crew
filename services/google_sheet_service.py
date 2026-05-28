import gspread
from google.oauth2.service_account import Credentials
from models.room import Room
from models.menu_item import MenuItem
from models.chat_message import ChatMessage
from .storage_service import StorageService

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

class GoogleSheetService(StorageService):
    def __init__(self, sheet_name):
        creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
        client = gspread.authorize(creds)
        self.spreadsheet = client.open(sheet_name)
        self.rooms_ws = self.spreadsheet.worksheet('rooms')
        self.members_ws = self.spreadsheet.worksheet('members')
        self.menu_ws = self.spreadsheet.worksheet('menu_items')
        self.chat_ws = self.spreadsheet.worksheet('chat_messages')

    def load_rooms(self):
        room_rows = self.rooms_ws.get_all_records()
        member_rows = self.members_ws.get_all_records()
        menu_rows = self.menu_ws.get_all_records()
        chat_rows = self.chat_ws.get_all_records()

        rooms = []
        for r in room_rows:
            room_id = int(r['room_id'])

            members = [
                row['member_name']
                for row in member_rows
                if int(row['room_id']) == room_id
            ]

            menu_items = [
                MenuItem(
                    item_id=int(row['menu_id']),
                    name=row['menu_name'],
                    price=int(row['price']),
                    quantity=int(row['quantity'])
                )
                for row in menu_rows
                if int(row['room_id']) == room_id
            ]

            chat_messages = [
                ChatMessage(
                    sender_name=row['user_name'],
                    message=row['message'],
                    created_at=row['created_at']
                )
                for row in chat_rows
                if int(row['room_id']) == room_id
            ]

            room = Room(
                room_id=room_id,
                title=r['title'],
                host_name=r['host_name'],
                target_people=int(r['target_people']),
                max_people=int(r['max_people']),
                order_type=r['order_type'],
                deadline_minutes=int(r['deadline_minutes']),
                meal_time=r['meal_time'],
                status=r['status'],
                members=members,
                menu_items=menu_items,
                chat_messages=chat_messages,
            )
            rooms.append(room)

        return rooms

    def save_rooms(self, rooms):
        self.rooms_ws.resize(1)
        self.members_ws.resize(1)
        self.menu_ws.resize(1)
        self.chat_ws.resize(1)

        room_rows, member_rows, menu_rows, chat_rows = [], [], [], []

        for room in rooms:
            room_rows.append([
                room.room_id, room.title, room.host_name,
                room.target_people, room.max_people, room.order_type,
                room.deadline_minutes, room.meal_time, room.status
            ])
            for member in room.members:
                member_rows.append([room.room_id, member])
            for item in room.menu_items:
                menu_rows.append([
                    room.room_id, item.item_id, item.name, item.price, item.quantity
                ])
            for chat in room.chat_messages:
                chat_rows.append([
                    room.room_id, chat.sender_name, chat.message, chat.created_at
                ])

        if room_rows:
            self.rooms_ws.append_rows(room_rows)
        if member_rows:
            self.members_ws.append_rows(member_rows)
        if menu_rows:
            self.menu_ws.append_rows(menu_rows)
        if chat_rows:
            self.chat_ws.append_rows(chat_rows)