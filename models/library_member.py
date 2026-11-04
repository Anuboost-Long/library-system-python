"""Library member model built on the shared person details."""

from datetime import date, datetime

from models.person import Person
from utils.check_date_valid import check_date_validity


class LibraryMember(Person):
    """Represent a registered library member and their membership details."""

    def __init__(
        self,
        name: str,
        dob: str,
        email: str,
        phone: str,
        member_id: str,
        registered_at: str,
    ):
        """Create a member with a unique member ID and registration date."""
        super().__init__(name=name, dob=dob, phone=phone, email=email)
        self.member_id = member_id
        self.registered_at = registered_at

    @property
    def member_id(self):
        return self.__member_id

    @member_id.setter
    def member_id(self, value):
        if hasattr(self, "_LibraryMember__member_id"):
            raise AttributeError("Member ID cannot be changed")

        if not isinstance(value, str) or not value.strip().startswith("Tor"):
            raise ValueError("Invalid Member Id")

        self.__member_id = value.strip()

    @property
    def registered_at(self):
        return self.__registered_at

    @registered_at.setter
    def registered_at(self, value):
        if not check_date_validity(value=value, max_date=date.today()):
            raise ValueError("Invalid date")
        self.__registered_at = datetime.strptime(value, "%d/%m/%Y").date()

    def describe(self) -> str:
        return (
            f"Member ID: {self.member_id}\n"
            f"Membership type: {self.membership_name}\n"
            f"Registered: {self.registered_at:%d/%m/%Y}\n"
            f"{super().describe()}"
        )

    @property
    def membership_name(self) -> str:
        raise NotImplementedError

    def loan_period(self) -> int:
        raise NotImplementedError

    def borrowing_limit(self) -> int:
        raise NotImplementedError


class NormalMember(LibraryMember):
    @property
    def membership_name(self) -> str:
        return "Normal"

    def loan_period(self) -> int:
        return 7

    def borrowing_limit(self) -> int:
        return 5


class PremiumMember(LibraryMember):
    @property
    def membership_name(self) -> str:
        return "Premium"

    def loan_period(self) -> int:
        return 14

    def borrowing_limit(self) -> int:
        return 7
