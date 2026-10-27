"""Application entry point for the library management system."""

from ui.start_menu import show_start_menu
from ui.quit import show_quit_menu
from ui.register_menu import show_register_menu
from ui.member_list import show_member_list
from ui.add_item_menu import show_add_item_menu
from ui.item_list import show_item_list
from services.library.library_service import LibraryService
from services.member.member_service import MemberService


def Main():
    """Keep the main menu available until the user chooses to quit."""
    member_service = MemberService()
    library_service = LibraryService()

    while True:
        option = show_start_menu()
        if option == 0:
            show_quit_menu()
            break
        if option == 2:
            show_register_menu(member_service)
        if option == 3:
            show_member_list(member_service)
        if option == 4:
            show_add_item_menu(library_service)
        if option == 5:
            show_item_list(library_service)


Main()
