from constants.theme import GREEN, RESET
from models.library_member import LibraryMember
from services.member.member_service import MemberService
from ui.prompts import show_error, show_header


MEMBERS_PER_PAGE = 10


def show_member_list(member_service: MemberService) -> None:
    """Show registered members in manageable pages."""
    empty_state = [
        "No members registered yet.",
        "Register a member to view their details here.",
    ]
    offset = 0
    query = ""

    while True:
        all_members = member_service.get_all_members()

        if not all_members:
            show_header("Member list")
            for line in empty_state:
                print(line)
            print("\n[Enter] Back")
            input(f"\n{GREEN}>{RESET} Press Enter to go back: ")
            return

        members = [
            member
            for member in all_members
            if query.casefold() in member.name.casefold()
        ]

        if not members:
            show_error(f'No members found with the name "{query}".')
            query = ""
            offset = 0
            continue

        page_members = members[offset : offset + MEMBERS_PER_PAGE]
        page = offset // MEMBERS_PER_PAGE + 1
        page_count = (len(members) - 1) // MEMBERS_PER_PAGE + 1
        has_previous = offset > 0
        has_next = offset + len(page_members) < len(members)
        controls = ["[P]  Previous"] if has_previous else []

        if has_next:
            controls.append("[N]  Next")

        controls.append("[S]  Search by name")

        if query:
            controls.append("[A]  Show all members")

        controls.append("[Enter]  Back")
        heading = f"Member list · Page {page} of {page_count}"

        if query:
            heading = f'{heading} · Search: "{query}"'

        show_header(heading)

        for index, member in enumerate(page_members):
            if index:
                print("-" * 44)

            print(member.describe())

        print("-" * 44)
        for control in controls:
            print(control)
        choice = input(f"\n{GREEN}>{RESET} Select an option: ").strip().lower()

        if choice == "s":
            query = input(f"{GREEN}>{RESET} Member name: ").strip()
            offset = 0
            continue

        if choice == "a" and query:
            query = ""
            offset = 0
            continue

        if not choice or choice == "b":
            return

        if choice == "p" and has_previous:
            offset -= MEMBERS_PER_PAGE
            continue

        if choice == "n" and has_next:
            offset += MEMBERS_PER_PAGE
            continue

        show_error("Choose one of the listed options.")
