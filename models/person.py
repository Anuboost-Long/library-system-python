"""Base model for people stored by the library system."""

from utils.check_date_valid import check_date_validity
from datetime import date, datetime


class Person:
    """Store and validate a person's contact details."""

    def __init__(self, name: str, dob: str, phone: str, email: str):
        """Create a person from validated identity and contact information."""
        self.name = name
        self.dob = dob
        self.phone = phone
        self.email = email

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self.__name = value.strip()

    @property
    def dob(self):
        return self.__dob

    @dob.setter
    def dob(self, value: str):
        if not check_date_validity(value=value.strip(), max_date=date.today()):
            raise ValueError("Invalid date of birth")
        self.__dob = datetime.strptime(value, "%d/%m/%Y").date()

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value: str):
        if not value.strip():
            raise ValueError("Phone cannot be empty")
        self.__phone = value.strip()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value: str):
        if "@" not in value.strip():
            raise ValueError("Invalid email")
        self.__email = value.strip()

    def describe(self) -> str:
        return f"Name: {self.name}, Email: {self.email}"
