from models.library_item import LibraryItem


class LibraryService:
    def __init__(self):
        self.__items: dict[str, LibraryItem] = {}

    def add_item(self, item: LibraryItem) -> None:
        if item.item_id in self.__items:
            raise ValueError("Item already exists")

        self.__items[item.item_id] = item

    def add_items(self, items: list[LibraryItem]) -> None:
        """Add a batch of items after confirming every ID is unique."""
        item_ids = [item.item_id for item in items]

        if len(item_ids) != len(set(item_ids)) or any(
            item_id in self.__items for item_id in item_ids
        ):
            raise ValueError("Item already exists")

        self.__items.update({item.item_id: item for item in items})

    def get_item(self, item_id: str) -> LibraryItem | None:
        return self.__items.get(item_id)

    def get_all_items(self) -> list[LibraryItem]:
        return list(self.__items.values())

    def get_items(self, offset: int, limit: int) -> list[LibraryItem]:
        """Return one insertion-ordered page of library items."""
        if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0:
            raise ValueError("Offset must be a non-negative integer")

        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError("Limit must be a positive integer")

        return list(self.__items.values())[offset : offset + limit]
