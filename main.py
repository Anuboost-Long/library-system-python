"""Application entry point for the library management system."""

from ui.start_menu import show_start_menu
from ui.quit import show_quit_menu
from ui.register_menu import show_register_menu
from ui.member_list import show_member_list
from ui.add_item_menu import show_add_item_menu
from ui.item_list import show_item_list
from services.library.library_service import LibraryService
from services.library.library_seed import seed_library_items
from services.loan.loan_service import LoanService
from services.loan.loan_seed import seed_loans
from services.member.member_seed import seed_members
from services.member.member_service import MemberService
from ui.borrow_menu import show_borrow_menu
from ui.loan_list import show_loan_list_menu


def Main():
    """Keep the main menu available until the user chooses to quit."""
    member_service = MemberService()
    library_service = LibraryService()
    seed_library_items(library_service)
    seed_members(member_service)
    loan_service = LoanService(library_service, member_service)
    seed_loans(loan_service)

    while True:
        option = show_start_menu()
        if option == 0:
            show_quit_menu()
            break
        if option == 1:
            show_borrow_menu(loan_service, member_service, library_service)
        if option == 2:
            show_register_menu(member_service)
        if option == 3:
            show_member_list(member_service)
        if option == 4:
            show_add_item_menu(library_service)
        if option == 5:
            show_item_list(library_service)
        if option == 6:
            show_loan_list_menu(loan_service, member_service)


Main()
