from datetime import date

from constants.theme import GREEN, RESET
from models.library_member import LibraryMember, NormalMember, PremiumMember
from services.member.member_service import MemberService
from ui.prompts import ask, show_error, show_header, show_success
from utils.check_date_valid import check_date_validity


def ask_date_of_birth() -> str:
    while True:
        dob = ask("Date of Birth", "DD/MM/YYYY")

        if check_date_validity(dob.strip(), max_date=date.today()):
            return dob.strip()

        show_error("Enter a valid date of birth in DD/MM/YYYY.")


def ask_member_type() -> type[LibraryMember]:
    choices = {
        "1": NormalMember,
        "2": PremiumMember,
    }

    while True:
        choice = ask("Membership type", "1. Normal  2. Premium")
        member_type = choices.get(choice)

        if member_type is not None:
            return member_type

        show_error("Choose 1 for Normal or 2 for Premium.")


def collect_member() -> LibraryMember:
    while True:
        name = ask("Full Name")
        dob = ask_date_of_birth()
        email = ask("Email Address")
        phone = ask("Phone Number")
        member_id = ask("Member ID", "Example: Tor001")
        member_type = ask_member_type()

        try:
            return member_type(
                name=name,
                dob=dob,
                email=email,
                phone=phone,
                member_id=member_id,
                registered_at=date.today().strftime("%d/%m/%Y"),
            )
        except ValueError as error:
            show_error(str(error))


def show_register_menu(member_service: MemberService) -> None:
    while True:
        show_header("Register a member", "Enter the member details below.")
        print("[Enter] Register member")
        print("[B] Back")

        choice = input(f"\n{GREEN}>{RESET} Select an option: ").strip().lower()

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
