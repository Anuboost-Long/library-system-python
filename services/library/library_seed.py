from models.library_item import LibraryItem
from services.library.library_service import LibraryService


SEED_ITEMS = (
    ("BK001", "Pride and Prejudice", "Book", "Jane Austen"),
    ("BK002", "1984", "Book", "George Orwell"),
    ("BK003", "To Kill a Mockingbird", "Book", "Harper Lee"),
    ("BK004", "The Great Gatsby", "Book", "F. Scott Fitzgerald"),
    ("BK005", "The Hobbit", "Book", "J. R. R. Tolkien"),
    ("BK006", "Jane Eyre", "Book", "Charlotte Bronte"),
    ("BK007", "The Catcher in the Rye", "Book", "J. D. Salinger"),
    ("BK008", "The Book Thief", "Book", "Markus Zusak"),
    ("BK009", "Little Women", "Book", "Louisa May Alcott"),
    ("BK010", "The Alchemist", "Book", "Paulo Coelho"),
    ("BK011", "Dune", "Book", "Frank Herbert"),
    ("BK012", "The Handmaid's Tale", "Book", "Margaret Atwood"),
    ("BK013", "The Martian", "Book", "Andy Weir"),
    ("BK014", "Where the Crawdads Sing", "Book", "Delia Owens"),
    ("BK015", "Atomic Habits", "Book", "James Clear"),
    ("BK016", "Sapiens", "Book", "Yuval Noah Harari"),
    ("BK017", "Educated", "Book", "Tara Westover"),
    ("BK018", "Project Hail Mary", "Book", "Andy Weir"),
    ("BK019", "Klara and the Sun", "Book", "Kazuo Ishiguro"),
    ("BK020", "Tomorrow, and Tomorrow, and Tomorrow", "Book", "Gabrielle Zevin"),
)


def seed_library_items(library_service: LibraryService) -> None:
    """Load the default catalogue without duplicating existing item IDs."""
    items = []

    for item_id, name, item_type, author in SEED_ITEMS:
        if library_service.get_item(item_id) is None:
            items.append(
                LibraryItem(
                    item_id=item_id,
                    name=name,
                    item_type=item_type,
                    author=author,
                )
            )

    library_service.add_items(items)
