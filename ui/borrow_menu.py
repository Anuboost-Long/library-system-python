from constants.theme import GREEN, RESET
from models.library_member import LibraryMember
from services.library.library_service import LibraryService
from services.loan.loan_service import LoanService
from services.member.member_service import MemberService
from ui.prompts import show_error, show_header, show_success


RECORDS_PER_PAGE = 10


def show_borrow_menu(
    loan_service: LoanService,
    member_service: MemberService,
    library_service: LibraryService,
) -> None:
    member = select_member(member_service)

    if member is None:
        return

    item_ids = select_items(loan_service, member, library_service)

    if not item_ids:
        return

    try:
        loans = loan_service.create_loans(member.member_id, item_ids)
    except ValueError as error:
        show_error(str(error))
        return

    show_success(f"Borrowed {len(loans)} item(s) for {member.name}.")


def select_member(member_service: MemberService) -> LibraryMember | None:
    offset = 0

    while True:
        total_members = len(member_service.get_all_members())

        if total_members == 0:
            show_error("No members are registered. Register a member first.")
            return None

        members = member_service.get_members(offset, RECORDS_PER_PAGE)
        page = offset // RECORDS_PER_PAGE + 1
        page_count = (total_members - 1) // RECORDS_PER_PAGE + 1
        has_previous = offset > 0
        has_next = offset + len(members) < total_members
        controls = ["[P]  Previous"] if has_previous else []

        if has_next:
            controls.append("[N]  Next")

        controls.append("[B]  Back")
        show_header(f"Select member · Page {page} of {page_count}")

        for index, member in enumerate(members):
            if index:
                print("-" * 44)

            print(member.describe())

        print("-" * 44)
        for control in controls:
            print(control)
        choice = input(
            f"\n{GREEN}>{RESET} Enter a member ID or select an option: "
        ).strip()
        member = member_service.get_member(choice)

        if member is not None:
            return member

        choice = choice.lower()

        if choice == "b":
            return None

        if choice == "p" and has_previous:
            offset -= RECORDS_PER_PAGE
            continue

        if choice == "n" and has_next:
            offset += RECORDS_PER_PAGE
            continue

        show_error("Enter a member ID from the list or choose a listed option.")


def select_items(
    loan_service: LoanService,
    member: LibraryMember,
    library_service: LibraryService,
) -> list[str]:
    selected_item_ids: list[str] = []
    offset = 0
    slots = loan_service.available_item_slots(member)

    if slots == 0:
        show_error(f"{member.name} has reached their borrowing limit.")
        return []

    while True:
        items = library_service.get_all_items()

        if not items:
            show_error("No items have been added yet.")
            return []

        page_items = items[offset : offset + RECORDS_PER_PAGE]
        page = offset // RECORDS_PER_PAGE + 1
        page_count = (len(items) - 1) // RECORDS_PER_PAGE + 1
        has_previous = offset > 0
        has_next = offset + len(page_items) < len(items)
        controls = ["[P]  Previous"] if has_previous else []

        if has_next:
            controls.append("[N]  Next")

        if selected_item_ids:
            controls.append("[C]  Confirm")

        controls.append("[B]  Cancel")
        heading = (
            f"Select items for {member.name} · "
            f"{len(selected_item_ids)} of {slots} selected · "
            f"Page {page} of {page_count}"
        )
        show_header(heading)

        for index, item in enumerate(page_items):
            if index:
                print("-" * 44)

            print(item.describe())

        if selected_item_ids:
            print(f"\nSelected: {', '.join(selected_item_ids)}")

        print("-" * 44)
        for control in controls:
            print(control)
        choice = input(
            f"\n{GREEN}>{RESET} Enter an item ID or select an option: "
        ).strip()

        if choice.lower() == "b":
            return []

        if choice.lower() == "c" and selected_item_ids:
            return selected_item_ids

        if choice.lower() == "p" and has_previous:
            offset -= RECORDS_PER_PAGE
            continue

        if choice.lower() == "n" and has_next:
            offset += RECORDS_PER_PAGE
            continue

        if choice in selected_item_ids:
            show_error("That item is already selected.")
            continue

        item = library_service.get_item(choice)

        if item is None or not item.is_available:
            show_error("Enter an available item ID from the list or choose an option.")
            continue

        if len(selected_item_ids) == slots:
            show_error(f"You can select up to {slots} item(s) for this member.")
            continue

        selected_item_ids.append(item.item_id)
