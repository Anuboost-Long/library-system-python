from models.library_item import LibraryItem


class LibraryService:
    def __init__(self):
        self.__items: dict[str, LibraryItem] = {}

    def add_item(self, item: LibraryItem) -> None:
        if item.item_id in self.__items:
            raise ValueError("Item already exists")

        self.__items[item.item_id] = item

    def get_item(self, item_id: str) -> LibraryItem | None:
        return self.__items.get(item_id)

    def get_all_items(self) -> list[LibraryItem]:
        return list(self.__items.values())
