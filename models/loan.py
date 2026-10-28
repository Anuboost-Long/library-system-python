from datetime import datetime


class Loan:
    def __init__(
        self,
        loan_id: str,
        member_id: str,
        item_id: str,
        borrow_date: datetime,
        due_date: datetime,
        return_date: datetime | None = None,
    ):
        self.loan_id = self.validate_id("Loan ID", loan_id)
        self.member_id = self.validate_id("Member ID", member_id)
        self.item_id = self.validate_id("Item ID", item_id)
        self.borrow_date = self.validate_date("Borrow date", borrow_date)
        self.due_date = self.validate_date("Due date", due_date)
        self.return_date = self.validate_optional_date(return_date)

        if self.due_date < self.borrow_date:
            raise ValueError("Due date cannot be before the borrow date")

        if self.return_date is not None and self.return_date < self.borrow_date:
            raise ValueError("Return date cannot be before the borrow date")

    @staticmethod
    def validate_id(label: str, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label} cannot be empty")

        return value.strip()

    @staticmethod
    def validate_date(label: str, value: datetime) -> datetime:
        if not isinstance(value, datetime):
            raise ValueError(f"{label} must be a timestamp")

        return value

    @classmethod
    def validate_optional_date(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None

        return cls.validate_date("Return date", value)

    def is_overdue(self, now: datetime | None = None) -> bool:
        return self.return_date is None and self.due_date < (now or datetime.now())
