from constants.theme import GREEN, RESET
from services.library.library_service import LibraryService
from ui.prompts import show_error, show_header

ITEMS_PER_PAGE = 10


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
            show_header("Item list")
            for line in empty_state:
                print(line)
            print("\n[Enter] Back")
            input(f"\n{GREEN}>{RESET} Press Enter to go back: ")
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

        show_header(heading)

        for index, item in enumerate(page_items):
            if index:
                print("-" * 44)

            print(item.describe())

        print("-" * 44)
        for control in controls:
            print(control)
        choice = input(f"\n{GREEN}>{RESET} Select an option: ").strip().lower()

        if choice == "s":
            query = input(f"{GREEN}>{RESET} Item name: ").strip()
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
