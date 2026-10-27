from constants.theme import CYAN, GREEN, RESET
from models.library_item import LibraryItem
from services.library.library_service import LibraryService
from ui.components import Container
from ui.prompts import ask, show_error, show_success


def collect_item() -> LibraryItem:
    while True:
        item_id = ask("Item ID", "Example: BK001")
        name = ask("Name")
        item_type = ask("Item type", "Example: Book")
        author = ask("Author")

        try:
            return LibraryItem(
                item_id=item_id,
                name=name,
                item_type=item_type,
                author=author,
            )
        except ValueError as error:
            show_error(str(error))


def show_add_item_menu(library_service: LibraryService) -> None:
    def render_intro(container: Container) -> None:
        container.line()
        container.line("Add an item")
        container.line("Enter the item details below.")
        container.line()
        container.divider()
        container.line("[Enter]  Add item", f"{CYAN}[Enter]{RESET}  Add item")
        container.line("[B]      Back", f"{CYAN}[B]{RESET}      Back")

    while True:
        Container().show(render_intro)

        choice = input(f"\n  {GREEN}❯{RESET} Select an option: ").strip().lower()

        if choice == "b":
            return

        if choice:
            show_error("Press Enter to add an item or B to go back.")
            continue

        try:
            library_service.add_item(collect_item())
        except ValueError as error:
            show_error(str(error))
        else:
            show_success("Item added.")
