from dataclasses import dataclass, field
from math import ceil
from typing import Optional

from .chat_message import ChatMessage
from .menu_item import MenuItem

STATUS_RECRUITING = "모집중"
STATUS_ALMOST_FULL = "마감임박"
STATUS_COMPLETED = "완료"


@dataclass
class Room:
    room_id: int
    title: str
    host_name: str
    target_people: int
    order_type: str
    deadline_minutes: int
    meal_time: str
    max_people: Optional[int] = None
    status: str = STATUS_RECRUITING
    members: list[str] = field(default_factory=list)
    menu_items: list[MenuItem] = field(default_factory=list)
    chat_messages: list[ChatMessage] = field(default_factory=list)

    def __post_init__(self):
        if self.max_people is None:
            self.max_people = self.target_people
        if self.host_name and self.host_name not in self.members:
            self.members.insert(0, self.host_name)
        self.update_status()

    def remaining_seats(self):
        return max(self.target_people - len(self.members), 0)

    def remaining_max_seats(self):
        return max(self.max_people - len(self.members), 0)

    def update_status(self):
        if self.status == STATUS_COMPLETED:
            return
        threshold = max(1, ceil(self.target_people * 0.1))
        if self.remaining_seats() <= threshold:
            self.status = STATUS_ALMOST_FULL
        else:
            self.status = STATUS_RECRUITING

    def can_join(self, user_name):
        if self.status == STATUS_COMPLETED:
            return False, "완료된 방에는 참여할 수 없습니다."
        if user_name in self.members:
            return False, "이미 참여한 방입니다."
        if len(self.members) >= self.max_people:
            return False, "최대 인원을 초과했습니다."
        return True, ""

    def join(self, user_name):
        can_join, message = self.can_join(user_name)
        if not can_join:
            return False, message
        self.members.append(user_name)
        self.update_status()
        return True, "참여 완료."

    def add_menu_item(self, name, price, quantity=1):
        item_id = self.next_menu_item_id()
        self.menu_items.append(MenuItem(item_id, name, price, quantity))
        return item_id

    def edit_menu_item(self, item_id, name, price, quantity=1):
        item = self.find_menu_item(item_id)
        if item is None:
            return False, "존재하지 않는 메뉴 번호입니다."
        item.name = name
        item.price = price
        item.quantity = quantity
        return True, "메뉴를 수정했습니다."

    def delete_menu_item(self, item_id):
        item = self.find_menu_item(item_id)
        if item is None:
            return False, "존재하지 않는 메뉴 번호입니다."
        self.menu_items.remove(item)
        return True, "메뉴를 삭제했습니다."

    def find_menu_item(self, item_id):
        for item in self.menu_items:
            if item.item_id == item_id:
                return item
        return None

    def next_menu_item_id(self):
        if not self.menu_items:
            return 1
        return max(item.item_id for item in self.menu_items) + 1

    def add_chat_message(self, sender_name, message):
        self.chat_messages.append(ChatMessage.create(sender_name, message))

    def complete(self, user_name):
        if user_name != self.host_name:
            return False, "방장만 완료할 수 있습니다."
        self.status = STATUS_COMPLETED
        return True, "방을 완료했습니다."

    def total_price(self):
        return sum(item.price * item.quantity for item in self.menu_items)

    def split_payment(self):
        member_count = max(len(self.members), 1)
        return ceil(self.total_price() / member_count)

    def clone(
        self,
        new_room_id,
        host_name,
        title,
        target_people,
        max_people,
        order_type,
        deadline_minutes,
        meal_time,
        menu_item_ids,
    ):
        selected_items = []
        for old_item in self.menu_items:
            if old_item.item_id in menu_item_ids:
                selected_items.append(
                    MenuItem(
                        item_id=len(selected_items) + 1,
                        name=old_item.name,
                        price=old_item.price,
                        quantity=old_item.quantity,
                    )
                )
        return Room(
            room_id=new_room_id,
            title=title,
            host_name=host_name,
            target_people=target_people,
            max_people=max_people,
            order_type=order_type,
            deadline_minutes=deadline_minutes,
            meal_time=meal_time,
            menu_items=selected_items,
        )

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "title": self.title,
            "host_name": self.host_name,
            "target_people": self.target_people,
            "max_people": self.max_people,
            "order_type": self.order_type,
            "deadline_minutes": self.deadline_minutes,
            "meal_time": self.meal_time,
            "status": self.status,
            "members": self.members,
            "menu_items": [item.to_dict() for item in self.menu_items],
            "chat_messages": [message.to_dict() for message in self.chat_messages],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            room_id=int(data.get("room_id", 0)),
            title=data.get("title", ""),
            host_name=data.get("host_name", ""),
            target_people=int(data.get("target_people", 0)),
            max_people=int(data.get("max_people", data.get("target_people", 0))),
            order_type=data.get("order_type", ""),
            deadline_minutes=int(data.get("deadline_minutes", 0)),
            meal_time=data.get("meal_time", ""),
            status=data.get("status", STATUS_RECRUITING),
            members=list(data.get("members", [])),
            menu_items=[
                MenuItem.from_dict(item) for item in data.get("menu_items", [])
            ],
            chat_messages=[
                ChatMessage.from_dict(message)
                for message in data.get("chat_messages", [])
            ],
        )
