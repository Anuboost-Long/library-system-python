from datetime import date

from constants.theme import CYAN, GREEN, RESET
from models.library_member import LibraryMember
from models.membership_type import MembershipType
from services.member.member_service import MemberService
from ui.components import Container
from ui.prompts import ask, show_error, show_success
from utils.check_date_valid import check_date_validity


def ask_date_of_birth() -> str:
    while True:
        dob = ask("Date of Birth", "DD/MM/YYYY")

        if check_date_validity(dob.strip(), max_date=date.today()):
            return dob.strip()

        show_error("Enter a valid date of birth in DD/MM/YYYY.")


def ask_membership_type() -> MembershipType:
    choices = {
        "1": MembershipType.NORMAL,
        "2": MembershipType.PREMIUM,
    }

    while True:
        choice = ask("Membership type", "1. Normal  2. Premium")
        membership_type = choices.get(choice)

        if membership_type is not None:
            return membership_type

        show_error("Choose 1 for Normal or 2 for Premium.")


def collect_member() -> LibraryMember:
    while True:
        name = ask("Full Name")
        dob = ask_date_of_birth()
        email = ask("Email Address")
        phone = ask("Phone Number")
        member_id = ask("Member ID", "Example: Tor001")
        membership_type = ask_membership_type()

        try:
            return LibraryMember(
                name=name,
                dob=dob,
                email=email,
                phone=phone,
                member_id=member_id,
                membership_type=membership_type,
                registered_at=date.today().strftime("%d/%m/%Y"),
            )
        except ValueError as error:
            show_error(str(error))


def show_register_menu(member_service: MemberService) -> None:
    def render_intro(container: Container) -> None:
        container.line()
        container.line("Register a member")
        container.line("Enter the member details below.")
        container.line()
        container.divider()
        container.line(
            "[Enter]  Register member", f"{CYAN}[Enter]{RESET}  Register member"
        )
        container.line("[B]      Back", f"{CYAN}[B]{RESET}      Back")

    while True:
        Container().show(render_intro)

        choice = input(f"\n  {GREEN}❯{RESET} Select an option: ").strip().lower()

        if choice == "b":
            return

        if choice:
            show_error("Press Enter to register or B to go back.")
            continue

        try:
            member_service.register(collect_member())
        except ValueError as error:
            show_error(str(error))
        else:
            show_success("Member registered.")
