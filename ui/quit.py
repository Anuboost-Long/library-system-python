"""Farewell screen displayed when the user exits the application."""

from constants.theme import BOLD, GREEN, RESET
from ui.components import Container


def show_quit_menu() -> None:
    """Show the closing message inside the shared terminal container."""
    def render_quit_message(container: Container) -> None:
        container.line()
        container.line("Goodbye!", f"{GREEN}{BOLD}Goodbye!{RESET}")
        container.line("Thanks for using the library system.")
        container.line()

    Container().show(render_quit_message)
