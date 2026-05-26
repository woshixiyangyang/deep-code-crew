from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatMessage:
    sender_name: str
    message: str
    created_at: str

    @classmethod
    def create(cls, sender_name, message):
        return cls(
            sender_name=sender_name,
            message=message,
            created_at=datetime.now().isoformat(timespec="seconds"),
        )

    def to_dict(self):
        return {
            "sender_name": self.sender_name,
            "message": self.message,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            sender_name=data.get("sender_name", ""),
            message=data.get("message", ""),
            created_at=data.get("created_at", ""),
        )
