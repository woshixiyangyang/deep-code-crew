from dataclasses import dataclass


@dataclass
class MenuItem:
    item_id: int
    name: str
    price: int = 0
    quantity: int = 1

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            item_id=int(data.get("item_id", 0)),
            name=data.get("name", ""),
            price=int(data.get("price", 0)),
            quantity=int(data.get("quantity", 1)),
        )
