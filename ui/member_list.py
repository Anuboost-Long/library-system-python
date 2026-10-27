from constants.theme import DEFAULT_WIDTH, GREEN, RESET
from models.library_member import LibraryMember
from services.member.member_service import MemberService
from ui.components import Container


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
    details = [
        member_details(member) for member in member_service.get_all_members()
    ]
    empty_state = [
        "No members registered yet.",
        "Register a member to view their details here.",
    ]
    content = ["Member list", "[Enter]  Back", *empty_state]
    content.extend(line for group in details for line in group)
    width = max(
        DEFAULT_WIDTH,
        max(len(line) + 4 for line in content),
    )

    def render_members(container: Container) -> None:
        container.line()
        container.line("Member list")

        if not details:
            container.line()
            for line in empty_state:
                container.line(line)
        else:
            for index, lines in enumerate(details):
                container.divider()

                for line in lines:
                    container.line(line)

                if index == len(details) - 1:
                    container.divider()

        container.line()
        container.line("[Enter]  Back")

    Container(width=width).show(render_members)
    input(f"\n  {GREEN}❯{RESET} Press Enter to go back: ")
