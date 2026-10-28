class LibraryItem:
    def __init__(
        self,
        item_id: str,
        name: str,
        item_type: str,
        author: str | None = None,
        is_available: bool = True,
    ):
        self.item_id = item_id
        self.name = self.validate_value("Name", name)
        self.item_type = self.validate_value("Item type", item_type)
        self.author = self.validate_optional_value(author)
        self.is_available = self.validate_availability(is_available)

    @property
    def item_id(self) -> str:
        return self.__item_id

    @item_id.setter
    def item_id(self, value: str) -> None:
        if hasattr(self, "_LibraryItem__item_id"):
            raise AttributeError("Item ID cannot be changed")

        self.__item_id = self.validate_value("Item ID", value)

    @staticmethod
    def validate_value(label: str, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label} cannot be empty")

        return value.strip()

    @staticmethod
    def validate_optional_value(value: str | None) -> str | None:
        if value is None:
            return None

        if not isinstance(value, str):
            raise ValueError("Author must be a string")

        return value.strip() or None

    @staticmethod
    def validate_availability(value: bool) -> bool:
        if not isinstance(value, bool):
            raise ValueError("Availability must be a boolean")

        return value
