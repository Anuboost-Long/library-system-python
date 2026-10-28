"""Library member model built on the shared person details."""

from models.person import Person
from models.membership_type import MembershipType
from utils.check_date_valid import check_date_validity
from datetime import date, datetime


class LibraryMember(Person):
    """Represent a registered library member and their membership details."""

    def __init__(
        self,
        name: str,
        dob: str,
        email: str,
        phone: str,
        member_id: str,
        membership_type: MembershipType,
        registered_at: str,
    ):
        """Create a member with a unique member ID and registration date."""
        super().__init__(name=name, dob=dob, phone=phone, email=email)
        self.member_id = member_id
        self.membership_type = membership_type
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
    def membership_type(self):
        return self.__membership_type

    @membership_type.setter
    def membership_type(self, value: MembershipType):
        if not isinstance(value, MembershipType):
            raise ValueError("Invalid membership type")
        self.__membership_type = value

    @property
    def registered_at(self):
        return self.__registered_at

    @registered_at.setter
    def registered_at(self, value):
        if not check_date_validity(value=value, max_date=date.today()):
            raise ValueError("Invalid date")
        self.__registered_at = datetime.strptime(value, "%d/%m/%Y").date()

    def describe(self):
        """Return a short summary suitable for a compact member listing."""
        return f"Member ID: {self.member_id}, Name: {self.name}"
