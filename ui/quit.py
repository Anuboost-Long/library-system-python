"""Farewell screen displayed when the user exits the application."""

from ui.prompts import show_header


def show_quit_menu() -> None:
    """Show the closing message."""
    show_header("Goodbye!")
    print("Thanks for using the library system.")
