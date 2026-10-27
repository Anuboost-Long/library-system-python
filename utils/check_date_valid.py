"""Date validation shared by the library member models and registration flow."""

from datetime import date


def check_date_validity(value: str, max_date: date | None = None) -> bool:
    """Return whether a DD/MM/YYYY value is a real date within an optional upper bound."""
    parts = value.split("/")

    if len(parts) != 3:
        return False

    day, month, year = parts

    if (len(day), len(month), len(year)) != (2, 2, 4):
        return False

    if not all(part.isascii() and part.isdigit() for part in parts):
        return False

    try:
        check_date = date(int(year), int(month), int(day))
        return max_date is None or check_date <= max_date
    except ValueError:
        return False
