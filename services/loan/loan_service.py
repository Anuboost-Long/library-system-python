from datetime import datetime, timedelta

from models.library_item import LibraryItem
from models.library_member import LibraryMember
from models.loan import Loan
from models.membership_type import MembershipType
from services.library.library_service import LibraryService
from services.member.member_service import MemberService


class LoanService:
    def __init__(
        self, library_service: LibraryService, member_service: MemberService
    ) -> None:
        self.__library_service = library_service
        self.__member_service = member_service
        self.__loans: dict[str, Loan] = {}

    def create_loan(
        self,
        member: LibraryMember | str,
        item: LibraryItem | str,
        borrowed_at: datetime | None = None,
    ) -> Loan:
        return self.create_loans(member, [item], borrowed_at)[0]

    def create_loans(
        self,
        member: LibraryMember | str,
        items: list[LibraryItem | str],
        borrowed_at: datetime | None = None,
    ) -> list[Loan]:
        library_member = self.resolve_member(member)
        library_items = [self.resolve_item(item) for item in items]

        if not library_items:
            raise ValueError("Choose at least one item")

        item_ids = [item.item_id for item in library_items]

        if len(item_ids) != len(set(item_ids)):
            raise ValueError("Choose each item only once")

        if len(library_items) > self.available_item_slots(library_member):
            raise ValueError("Member has reached their borrowing limit")

        if any(not item.is_available for item in library_items):
            raise ValueError("Item is not available")

        if borrowed_at is not None and not isinstance(borrowed_at, datetime):
            raise ValueError("Borrow date must be a timestamp")

        borrow_date = borrowed_at or datetime.now()
        loans = []

        for library_item in library_items:
            loan = Loan(
                loan_id=f"LN{len(self.__loans) + 1:03}",
                member_id=library_member.member_id,
                item_id=library_item.item_id,
                borrow_date=borrow_date,
                due_date=borrow_date
                + timedelta(days=self.loan_period(library_member)),
            )
            self.__loans[loan.loan_id] = loan
            library_item.is_available = False
            loans.append(loan)

        return loans

    def get_loan(self, loan_id: str) -> Loan | None:
        return self.__loans.get(loan_id)

    def get_all_loans(self) -> list[Loan]:
        return list(self.__loans.values())

    def get_active_loans(
        self, member_id: str | None = None, item_id: str | None = None
    ) -> list[Loan]:
        return [
            loan
            for loan in self.__loans.values()
            if loan.return_date is None
            and (member_id is None or loan.member_id == member_id)
            and (item_id is None or loan.item_id == item_id)
        ]

    def get_overdue_loans(self) -> list[Loan]:
        return [loan for loan in self.get_active_loans() if loan.is_overdue()]

    def get_loans_for_member(self, member: LibraryMember | str) -> list[Loan]:
        library_member = self.resolve_member(member)
        return [
            loan
            for loan in self.__loans.values()
            if loan.member_id == library_member.member_id
        ]

    def available_item_slots(self, member: LibraryMember | str) -> int:
        library_member = self.resolve_member(member)
        active_loans = sum(
            loan.member_id == library_member.member_id and loan.return_date is None
            for loan in self.__loans.values()
        )
        return self.borrowing_limit(library_member) - active_loans

    def return_loan(self, loan: Loan | str) -> Loan:
        return self.return_loans([loan])[0]

    def return_loans(self, loans: list[Loan | str]) -> list[Loan]:
        library_loans = [self.resolve_loan(loan) for loan in loans]

        if not library_loans:
            raise ValueError("Choose at least one loan")

        loan_ids = [loan.loan_id for loan in library_loans]

        if len(loan_ids) != len(set(loan_ids)):
            raise ValueError("Choose each loan only once")

        if any(loan.return_date is not None for loan in library_loans):
            raise ValueError("Loan has already been returned")

        library_items = [self.resolve_item(loan.item_id) for loan in library_loans]
        returned_at = datetime.now()

        for loan, item in zip(library_loans, library_items):
            loan.return_date = returned_at
            item.is_available = True

        return library_loans

    def resolve_loan(self, loan: Loan | str) -> Loan:
        if isinstance(loan, Loan):
            return loan

        if isinstance(loan, str):
            library_loan = self.get_loan(loan)
            if library_loan is not None:
                return library_loan

        raise ValueError("Loan not found")

    def resolve_member(self, member: LibraryMember | str) -> LibraryMember:
        if isinstance(member, LibraryMember):
            member = member.member_id

        if isinstance(member, str):
            registered_member = self.__member_service.get_member(member)
            if registered_member is not None:
                return registered_member

        raise ValueError("Member not found")

    def resolve_item(self, item: LibraryItem | str) -> LibraryItem:
        if isinstance(item, LibraryItem):
            item = item.item_id

        if isinstance(item, str):
            library_item = self.__library_service.get_item(item)
            if library_item is not None:
                return library_item

        raise ValueError("Item not found")

    @staticmethod
    def loan_period(member: LibraryMember) -> int:
        if member.membership_type is MembershipType.PREMIUM:
            return 14

        return 7

    @staticmethod
    def borrowing_limit(member: LibraryMember) -> int:
        if member.membership_type is MembershipType.PREMIUM:
            return 7

        return 5
