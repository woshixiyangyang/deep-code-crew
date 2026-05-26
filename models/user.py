from dataclasses import dataclass


@dataclass
class User:
    name: str

    def to_dict(self):
        return {"name": self.name}

    @classmethod
    def from_dict(cls, data):
        return cls(name=data.get("name", ""))
