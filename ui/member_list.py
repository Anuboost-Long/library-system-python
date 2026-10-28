from constants.theme import DEFAULT_WIDTH, GREEN, RESET
from models.library_member import LibraryMember
from services.member.member_service import MemberService
from ui.components import Container
from ui.prompts import show_error


MEMBERS_PER_PAGE = 10


def member_details(member: LibraryMember) -> list[str]:
    """Format all details for one member as readable terminal rows."""
    return [
        f"Member ID: {member.member_id}",
        f"Name: {member.name}",
        f"Membership type: {member.membership_type}",
        f"Date of birth: {member.dob:%d/%m/%Y}",
        f"Email: {member.email}",
        f"Phone: {member.phone}",
        f"Registered: {member.registered_at:%d/%m/%Y}",
    ]


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
            content = ["Member list", "[Enter]  Back", *empty_state]
            width = max(DEFAULT_WIDTH, max(len(line) + 4 for line in content))

            def render_empty_state(container: Container) -> None:
                container.line()
                container.line("Member list")
                container.line()
                for line in empty_state:
                    container.line(line)
                container.line()
                container.line("[Enter]  Back")

            Container(width=width).show(render_empty_state)
            input(f"\n  {GREEN}❯{RESET} Press Enter to go back: ")
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
        member_groups = [member_details(member) for member in page_members]
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

        content = [heading, *controls]
        content.extend(line for group in member_groups for line in group)
        width = max(DEFAULT_WIDTH, max(len(line) + 4 for line in content))

        def render_members(container: Container) -> None:
            container.line()
            container.line(heading)
            container.line()

            for index, lines in enumerate(member_groups):
                container.divider()

                for line in lines:
                    container.line(line)

                if index == len(member_groups) - 1:
                    container.divider()

            container.line()
            for control in controls:
                container.line(control)

        Container(width=width).show(render_members)
        choice = input(f"\n  {GREEN}❯{RESET} Select an option: ").strip().lower()

        if choice == "s":
            query = input(f"  {GREEN}❯{RESET} Member name: ").strip()
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
