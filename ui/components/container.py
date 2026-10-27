"""Reusable bordered container for terminal UI content."""

from collections.abc import Callable

from constants.theme import DEFAULT_WIDTH, GRAY, RESET


class Container:
    """Draw consistently styled terminal frames around supplied content."""

    def __init__(
        self,
        width: int = DEFAULT_WIDTH,
        border: str = GRAY,
        reset: str = RESET,
        indent: str = "  ",
    ):
        self.width = width
        self.border = border
        self.reset = reset
        self.indent = indent

    def show(self, render_contents: Callable[["Container"], None]) -> None:
        """Draw the frame before and after a callback renders its contents."""
        print(f"{self.indent}{self.border}╭{'─' * (self.width - 2)}╮{self.reset}")
        render_contents(self)
        print(f"{self.indent}{self.border}╰{'─' * (self.width - 2)}╯{self.reset}")

    def line(self, text: str = "", styled_text: str | None = None) -> None:
        """Draw one padded row, using styled text without affecting alignment."""
        padding = " " * max(0, self.width - 4 - len(text))
        content = styled_text if styled_text is not None else text
        print(
            f"{self.indent}{self.border}│{self.reset}  {content}{padding}{self.border}│{self.reset}"
        )

    def divider(self) -> None:
        """Draw a horizontal divider between groups of container content."""
        print(f"{self.indent}{self.border}├{'─' * (self.width - 2)}┤{self.reset}")
