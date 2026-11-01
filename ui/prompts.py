"""Shared terminal prompts and feedback messages."""

from constants.theme import BOLD, CYAN, GRAY, GREEN, RED, RESET


def show_header(title: str, subtitle: str = ""):
    """Print a section heading with an optional description."""
    print(f"\n{BOLD}{title}{RESET}")

    if subtitle:
        print(f"{GRAY}{subtitle}{RESET}")

    print(f"{GRAY}{'=' * 44}{RESET}")


def ask(label: str, hint: str = "") -> str:
    """Prompt for a value, optionally showing an expected format hint."""
    print(f"\n{CYAN}{BOLD}{label}{RESET}")

    if hint:
        print(f"{GRAY}{hint}{RESET}")

    return input(f"{GREEN}>{RESET} ").strip()


def show_error(message: str):
    """Display a validation or input error in the shared error style."""
    print(f"\n{RED}Error: {message}{RESET}")


def show_success(message: str):
    """Display a success confirmation in the shared success style."""
    print(f"\n{GREEN}{message}{RESET}")
