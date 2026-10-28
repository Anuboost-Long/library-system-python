"""Main navigation screen for the library management system."""

from ui.components import Container
from constants.theme import BOLD, CYAN, GRAY, GREEN, RED, RESET


def show_start_menu() -> int:
    """Show available actions and return the selected menu number."""
    while True:
        print()
        print(f"  {GREEN}◆{RESET} {BOLD}Library Management System{RESET}")
        print(f"  {GRAY}A workspace for managing library resources.{RESET}")
        print()

        options = [
            ("1", "Borrow Item"),
            ("2", "Register Member"),
            ("3", "Show All Members"),
            ("4", "Add Item"),
            ("5", "Show All Items"),
            ("6", "Loan List"),
        ]

        def render_menu(container: Container) -> None:
            container.line()
            container.line("WHAT WOULD YOU LIKE TO DO?")
            container.line()

            for number, label in options:
                text = f"[{number}]  {label}"
                styled = f"{CYAN}[{number}]{RESET}  {label}"
                container.line(text, styled)

            container.line()
            container.divider()
            container.line("[0]  Quit", f"{GRAY}[0]{RESET}  Quit")

        Container().show(render_menu)

        choice = input(f"\n  {GREEN}❯{RESET} Select an option: ").strip()

        if choice in ("0", "1", "2", "3", "4", "5", "6"):
            return int(choice)

        print(f"\n  {RED}✕ Invalid option. Please try again.{RESET}")
