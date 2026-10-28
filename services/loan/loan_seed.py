from datetime import datetime, timedelta

from services.loan.loan_service import LoanService


SEED_LOANS = (
    ("Tor001", "BK001", 8),
    ("Tor002", "BK002", 15),
    ("Tor003", "BK003", 3),
    ("Tor004", "BK004", 4),
    ("Tor005", "BK005", 1),
)


def seed_loans(loan_service: LoanService) -> None:
    seeded_item_ids = {loan.item_id for loan in loan_service.get_all_loans()}

    for member_id, item_id, days_ago in SEED_LOANS:
        if item_id not in seeded_item_ids:
            loan_service.create_loan(
                member_id,
                item_id,
                borrowed_at=datetime.now() - timedelta(days=days_ago),
            )
