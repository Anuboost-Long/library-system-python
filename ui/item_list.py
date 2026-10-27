from constants.theme import DEFAULT_WIDTH, GREEN, RESET
from models.library_item import LibraryItem
from services.library.library_service import LibraryService
from ui.components import Container


def item_details(item: LibraryItem) -> list[str]:
    return [
        f"Item ID: {item.item_id}",
        f"Name: {item.name}",
        f"Type: {item.item_type}",
        f"Author: {item.author or 'Not specified'}",
        f"Available: {'Yes' if item.is_available else 'No'}",
    ]


def show_item_list(library_service: LibraryService) -> None:
    details = [item_details(item) for item in library_service.get_all_items()]
    empty_state = [
        "No items added yet.",
        "Add an item to view its details here.",
    ]
    content = ["Item list", "[Enter]  Back", *empty_state]
    content.extend(line for group in details for line in group)
    width = max(DEFAULT_WIDTH, max(len(line) + 4 for line in content))

    def render_items(container: Container) -> None:
        container.line()
        container.line("Item list")

        if not details:
            container.line()
            for line in empty_state:
                container.line(line)
        else:
            for index, lines in enumerate(details):
                container.divider()

                for line in lines:
                    container.line(line)

                if index == len(details) - 1:
                    container.divider()

        container.line()
        container.line("[Enter]  Back")

    Container(width=width).show(render_items)
    input(f"\n  {GREEN}❯{RESET} Press Enter to go back: ")
