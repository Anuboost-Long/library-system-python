from datetime import datetime

from constants.theme import CYAN, DEFAULT_WIDTH, GREEN, RED, RESET
from models.library_member import LibraryMember
from models.loan import Loan
from services.loan.loan_service import LoanService
from services.member.member_service import MemberService
from ui.borrow_menu import select_member
from ui.components import Container
from ui.prompts import show_error, show_success


LOANS_PER_PAGE = 10


def show_loan_list_menu(
    loan_service: LoanService, member_service: MemberService
) -> None:
    while True:
        def render_menu(container: Container) -> None:
            container.line()
            container.line("Loan list")
            container.line()
            container.line("[1]  All loans", f"{CYAN}[1]{RESET}  All loans")
            container.line(
                "[2]  Loans for a member",
                f"{CYAN}[2]{RESET}  Loans for a member",
            )
            container.line(
                "[3]  Return loans",
                f"{CYAN}[3]{RESET}  Return loans",
            )
            container.line(
                "[4]  Overdue items",
                f"{CYAN}[4]{RESET}  Overdue items",
            )
            container.line()
            container.divider()
            container.line("[B]  Back", f"{CYAN}[B]{RESET}  Back")

        Container().show(render_menu)
        choice = input(f"\n  {GREEN}❯{RESET} Select an option: ").strip().lower()

        if choice == "b":
            return

        if choice == "1":
            show_loans("All loans", loan_service.get_all_loans())
            continue

        if choice == "2":
            member = select_member(member_service)

            if member is not None:
                show_member_loans(loan_service, member)

            continue

        if choice == "3":
            show_return_loans(loan_service)
            continue

        if choice == "4":
            show_overdue_loans(loan_service)
            continue

        show_error("Choose 1, 2, 3, or 4, or B to go back.")


def show_member_loans(loan_service: LoanService, member: LibraryMember) -> None:
    show_loans(
        f"Loans for {member.name}",
        loan_service.get_loans_for_member(member),
    )


def show_overdue_loans(loan_service: LoanService) -> None:
    loans = loan_service.get_overdue_loans()

    if not loans:
        show_empty_loans(
            "Overdue items",
            "No overdue loans.",
            "All active loans are within their due date.",
        )
        return

    show_loans("Overdue items", loans)


def show_return_loans(loan_service: LoanService) -> None:
    offset = 0
    selected_loan_ids: list[str] = []
    search_field: str | None = None
    search_value: str | None = None

    while True:
        loans = active_loans(loan_service, search_field, search_value)

        if not loans:
            if search_value is None:
                show_error("No loans are currently awaiting return.")
                return

            show_error("No active loans match that search.")
            search_field = None
            search_value = None
            continue

        page_loans = loans[offset : offset + LOANS_PER_PAGE]
        page = offset // LOANS_PER_PAGE + 1
        page_count = (len(loans) - 1) // LOANS_PER_PAGE + 1
        has_previous = offset > 0
        has_next = offset + len(page_loans) < len(loans)
        controls = ["[P]  Previous"] if has_previous else []

        if has_next:
            controls.append("[N]  Next")

        controls.append("[S]  Search")

        if search_value is not None:
            controls.append("[A]  Show all active loans")

        if selected_loan_ids:
            controls.append("[C]  Confirm returns")

        controls.append("[B]  Back")
        loan_groups = [loan_details(loan) for loan in page_loans]
        heading = f"Return loans · {len(selected_loan_ids)} selected · Page {page} of {page_count}"
        content = [heading, *controls, *selected_loan_ids]
        content.extend(line for group in loan_groups for line in group)
        width = max(DEFAULT_WIDTH, max(len(line) + 4 for line in content))

        def render_loans(container: Container) -> None:
            container.line()
            container.line(heading)
            container.line()

            for index, (loan, lines) in enumerate(zip(page_loans, loan_groups)):
                container.divider()

                for line in lines:
                    container.line(line, styled_loan_line(line, loan))

                if index == len(loan_groups) - 1:
                    container.divider()

            if selected_loan_ids:
                container.line()
                container.line(f"Selected: {', '.join(selected_loan_ids)}")

            container.line()
            for control in controls:
                container.line(control)

        Container(width=width).show(render_loans)
        choice = input(
            f"\n  {GREEN}❯{RESET} Enter a loan ID or select an option: "
        ).strip()
        command = choice.lower()

        if command == "s":
            search_field, search_value = choose_search()
            offset = 0
            continue

        if command == "a" and search_value is not None:
            search_field = None
            search_value = None
            offset = 0
            continue

        if command == "c" and selected_loan_ids:
            try:
                returned_loans = loan_service.return_loans(selected_loan_ids)
            except ValueError as error:
                show_error(str(error))
                return

            show_success(f"Returned {len(returned_loans)} loan(s).")
            return

        if command == "b":
            return

        if command == "p" and has_previous:
            offset -= LOANS_PER_PAGE
            continue

        if command == "n" and has_next:
            offset += LOANS_PER_PAGE
            continue

        loan = loan_service.get_loan(choice)

        if (
            loan is None
            or loan.return_date is not None
            or loan.loan_id not in {active_loan.loan_id for active_loan in loans}
        ):
            show_error("Enter an active loan ID from the list or choose an option.")
            continue

        if loan.loan_id in selected_loan_ids:
            show_error("That loan is already selected.")
            continue

        selected_loan_ids.append(loan.loan_id)


def active_loans(
    loan_service: LoanService, search_field: str | None, search_value: str | None
) -> list[Loan]:
    if search_field == "member":
        return loan_service.get_active_loans(member_id=search_value)

    if search_field == "item":
        return loan_service.get_active_loans(item_id=search_value)

    return loan_service.get_active_loans()


def choose_search() -> tuple[str | None, str | None]:
    while True:
        choice = input(
            f"\n  {GREEN}❯{RESET} Search by [M]ember ID, [I]tem ID, or [B]ack: "
        ).strip().lower()

        if choice == "b":
            return None, None

        if choice == "m":
            return "member", input(f"  {GREEN}❯{RESET} Member ID: ").strip()

        if choice == "i":
            return "item", input(f"  {GREEN}❯{RESET} Item ID: ").strip()

        show_error("Choose M for member ID or I for item ID.")


def show_loans(title: str, loans: list[Loan]) -> None:
    if not loans:
        show_empty_loans(title, "No loans yet.", "Borrow an item to create a loan.")
        return

    offset = 0

    while True:
        page_loans = loans[offset : offset + LOANS_PER_PAGE]
        page = offset // LOANS_PER_PAGE + 1
        page_count = (len(loans) - 1) // LOANS_PER_PAGE + 1
        has_previous = offset > 0
        has_next = offset + len(page_loans) < len(loans)
        controls = ["[P]  Previous"] if has_previous else []

        if has_next:
            controls.append("[N]  Next")

        controls.append("[Enter]  Back")
        loan_groups = [loan_details(loan) for loan in page_loans]
        content = [f"{title} · Page {page} of {page_count}", *controls]
        content.extend(line for group in loan_groups for line in group)
        width = max(DEFAULT_WIDTH, max(len(line) + 4 for line in content))

        def render_loans(container: Container) -> None:
            container.line()
            container.line(f"{title} · Page {page} of {page_count}")
            container.line()

            for index, (loan, lines) in enumerate(zip(page_loans, loan_groups)):
                container.divider()

                for line in lines:
                    container.line(line, styled_loan_line(line, loan))

                if index == len(loan_groups) - 1:
                    container.divider()

            container.line()
            for control in controls:
                container.line(control)

        Container(width=width).show(render_loans)
        choice = input(f"\n  {GREEN}❯{RESET} Select an option: ").strip().lower()

        if not choice or choice == "b":
            return

        if choice == "p" and has_previous:
            offset -= LOANS_PER_PAGE
            continue

        if choice == "n" and has_next:
            offset += LOANS_PER_PAGE
            continue

        show_error("Choose one of the listed options.")


def show_empty_loans(title: str, message: str, help_text: str) -> None:
    content = [title, message, help_text, "[Enter]  Back"]
    width = max(DEFAULT_WIDTH, max(len(line) + 4 for line in content))

    def render_empty_loans(container: Container) -> None:
        container.line()
        container.line(title)
        container.line()
        container.line(message)
        container.line(help_text)
        container.line()
        container.line("[Enter]  Back")

    Container(width=width).show(render_empty_loans)
    input(f"\n  {GREEN}❯{RESET} Press Enter to go back: ")


def loan_details(loan: Loan) -> list[str]:
    status = "● Not returned"

    if loan.return_date is not None:
        status = f"● Returned · {loan.return_date:%d/%m/%Y %H:%M}"

    return [
        f"Loan ID: {loan.loan_id}",
        f"Member ID: {loan.member_id}",
        f"Item ID: {loan.item_id}",
        f"Borrowed: {loan.borrow_date:%d/%m/%Y %H:%M}",
        f"Due: {loan.due_date:%d/%m/%Y %H:%M}",
        f"Returned: {status}",
    ]


def styled_loan_line(line: str, loan: Loan) -> str:
    if line.startswith("Due:") and loan.return_date is None and loan.due_date < datetime.now():
        return f"{RED}{line}{RESET}"

    if not line.startswith("Returned:"):
        return line

    colour = GREEN if loan.return_date is not None else RED
    return f"Returned: {colour}{line.removeprefix('Returned: ')}{RESET}"
