from constants.theme import DEFAULT_WIDTH, GREEN, RED, RESET
from models.library_item import LibraryItem
from services.library.library_service import LibraryService
from ui.components import Container
from ui.prompts import show_error

ITEMS_PER_PAGE = 10


def item_details(item: LibraryItem) -> list[str]:
    return [
        f"Item ID: {item.item_id}",
        f"Name: {item.name}",
        f"Type: {item.item_type}",
        f"Author: {item.author or 'Not specified'}",
        f"Availability: {availability_label(item)}",
    ]


def show_item_list(library_service: LibraryService) -> None:
    """Show library items in manageable pages."""
    empty_state = [
        "No items added yet.",
        "Add an item to view its details here.",
    ]
    offset = 0
    query = ""

    while True:
        all_items = library_service.get_all_items()

        if not all_items:
            content = ["Item list", "[Enter]  Back", *empty_state]
            width = max(DEFAULT_WIDTH, max(len(line) + 4 for line in content))

            def render_empty_state(container: Container) -> None:
                container.line()
                container.line("Item list")
                container.line()
                for line in empty_state:
                    container.line(line)
                container.line()
                container.line("[Enter]  Back")

            Container(width=width).show(render_empty_state)
            input(f"\n  {GREEN}❯{RESET} Press Enter to go back: ")
            return

        items = [
            item for item in all_items if query.casefold() in item.name.casefold()
        ]

        if not items:
            show_error(f'No items found with the name "{query}".')
            query = ""
            offset = 0
            continue

        page_items = items[offset : offset + ITEMS_PER_PAGE]
        item_groups = [item_details(item) for item in page_items]
        page = offset // ITEMS_PER_PAGE + 1
        page_count = (len(items) - 1) // ITEMS_PER_PAGE + 1
        has_previous = offset > 0
        has_next = offset + len(page_items) < len(items)
        controls = ["[P]  Previous"] if has_previous else []

        if has_next:
            controls.append("[N]  Next")

        controls.append("[S]  Search by name")

        if query:
            controls.append("[A]  Show all items")

        controls.append("[Enter]  Back")
        heading = f"Item list · Page {page} of {page_count}"

        if query:
            heading = f'{heading} · Search: "{query}"'

        content = [heading, *controls]
        content.extend(line for group in item_groups for line in group)
        width = max(DEFAULT_WIDTH, max(len(line) + 4 for line in content))

        def render_items(container: Container) -> None:
            container.line()
            container.line(heading)
            container.line()

            for index, (item, lines) in enumerate(zip(page_items, item_groups)):
                container.divider()

                for line in lines:
                    styled_line = line

                    if line.startswith("Availability:"):
                        styled_line = (
                            f"Availability: {availability_indicator(item)}"
                        )

                    container.line(line, styled_line)

                if index == len(item_groups) - 1:
                    container.divider()

            container.line()
            for control in controls:
                container.line(control)

        Container(width=width).show(render_items)
        choice = input(f"\n  {GREEN}❯{RESET} Select an option: ").strip().lower()

        if choice == "s":
            query = input(f"  {GREEN}❯{RESET} Item name: ").strip()
            offset = 0
            continue

        if choice == "a" and query:
            query = ""
            offset = 0
            continue

        if not choice or choice == "b":
            return

        if choice == "p" and has_previous:
            offset -= ITEMS_PER_PAGE
            continue

        if choice == "n" and has_next:
            offset += ITEMS_PER_PAGE
            continue

        show_error("Choose one of the listed options.")


def availability_label(item: LibraryItem) -> str:
    return "● Available" if item.is_available else "● Unavailable"


def availability_indicator(item: LibraryItem) -> str:
    colour = GREEN if item.is_available else RED
    return f"{colour}{availability_label(item)}{RESET}"
