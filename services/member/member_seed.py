from models.library_member import LibraryMember
from models.membership_type import MembershipType
from services.member.member_service import MemberService


SEED_MEMBERS = (
    ("Ava Nguyen", "14/03/1998", "ava.nguyen@example.com", "0400 100 001", "Tor001", MembershipType.NORMAL, "12/01/2026"),
    ("Liam Wilson", "22/08/1987", "liam.wilson@example.com", "0400 100 002", "Tor002", MembershipType.PREMIUM, "18/01/2026"),
    ("Noah Patel", "06/11/2001", "noah.patel@example.com", "0400 100 003", "Tor003", MembershipType.NORMAL, "03/02/2026"),
    ("Mia Chen", "19/05/1994", "mia.chen@example.com", "0400 100 004", "Tor004", MembershipType.PREMIUM, "10/02/2026"),
    ("Ethan Brown", "27/01/1979", "ethan.brown@example.com", "0400 100 005", "Tor005", MembershipType.NORMAL, "24/02/2026"),
    ("Sofia Garcia", "11/07/1990", "sofia.garcia@example.com", "0400 100 006", "Tor006", MembershipType.PREMIUM, "05/03/2026"),
    ("Lucas Martin", "30/09/2003", "lucas.martin@example.com", "0400 100 007", "Tor007", MembershipType.NORMAL, "17/03/2026"),
    ("Isla Thompson", "02/12/1985", "isla.thompson@example.com", "0400 100 008", "Tor008", MembershipType.PREMIUM, "28/03/2026"),
    ("Oliver Davis", "16/04/1996", "oliver.davis@example.com", "0400 100 009", "Tor009", MembershipType.NORMAL, "09/04/2026"),
    ("Grace Lee", "25/06/1989", "grace.lee@example.com", "0400 100 010", "Tor010", MembershipType.PREMIUM, "20/04/2026"),
    ("Henry Walker", "08/02/1976", "henry.walker@example.com", "0400 100 011", "Tor011", MembershipType.NORMAL, "02/05/2026"),
    ("Ella King", "13/10/2000", "ella.king@example.com", "0400 100 012", "Tor012", MembershipType.PREMIUM, "15/05/2026"),
)


def seed_members(member_service: MemberService) -> None:
    members = []

    for member_data in SEED_MEMBERS:
        if member_service.get_member(member_data[4]) is None:
            members.append(LibraryMember(*member_data))

    member_service.register_members(members)
