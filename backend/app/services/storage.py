"""In-memory data storage for the API."""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import count
from typing import Any


@dataclass
class Repository:
    """Simple repository with auto-incrementing integer IDs."""

    _id_counter: Any = field(default_factory=lambda: count(1), init=False)
    items: dict[int, dict] = field(default_factory=dict)

    def create(self, payload: dict) -> dict:
        item_id = next(self._id_counter)
        item = {"id": item_id, **payload}
        self.items[item_id] = item
        return item

    def list(self) -> list[dict]:
        return list(self.items.values())

    def get(self, item_id: int) -> dict | None:
        return self.items.get(item_id)

    def update(self, item_id: int, payload: dict) -> dict | None:
        if item_id not in self.items:
            return None
        self.items[item_id] = {"id": item_id, **payload}
        return self.items[item_id]

    def delete(self, item_id: int) -> bool:
        return self.items.pop(item_id, None) is not None


meters_repo = Repository()
readings_repo = Repository()
invoices_repo = Repository()
settlements_repo = Repository()
