"""Main navigation screen for the library management system."""

from constants.theme import CYAN, GREEN, RED, RESET
from ui.prompts import show_header


def show_start_menu() -> int:
    """Show available actions and return the selected menu number."""
    while True:
        show_header(
            "Library Management System", "Manage your members, items, and loans."
        )

        options = [
            ("1", "Borrow Item"),
            ("2", "Register Member"),
            ("3", "Show All Members"),
            ("4", "Add Item"),
            ("5", "Show All Items"),
            ("6", "Loan List"),
        ]

        for number, label in options:
            print(f"{CYAN}{number}.{RESET} {label}")

        print("-" * 44)
        print("0. Quit")

        choice = input(f"\n{GREEN}>{RESET} Select an option: ").strip()

        if choice in ("0", "1", "2", "3", "4", "5", "6"):
            return int(choice)

        print(f"\n{RED}Error: Invalid option. Please try again.{RESET}")
