from models.library_member import LibraryMember, NormalMember, PremiumMember
from services.member.member_service import MemberService


SEED_MEMBERS = (
    (NormalMember, "Ava Nguyen", "14/03/1998", "ava.nguyen@example.com", "0400 100 001", "Tor001", "12/01/2026"),
    (PremiumMember, "Liam Wilson", "22/08/1987", "liam.wilson@example.com", "0400 100 002", "Tor002", "18/01/2026"),
    (NormalMember, "Noah Patel", "06/11/2001", "noah.patel@example.com", "0400 100 003", "Tor003", "03/02/2026"),
    (PremiumMember, "Mia Chen", "19/05/1994", "mia.chen@example.com", "0400 100 004", "Tor004", "10/02/2026"),
    (NormalMember, "Ethan Brown", "27/01/1979", "ethan.brown@example.com", "0400 100 005", "Tor005", "24/02/2026"),
    (PremiumMember, "Sofia Garcia", "11/07/1990", "sofia.garcia@example.com", "0400 100 006", "Tor006", "05/03/2026"),
    (NormalMember, "Lucas Martin", "30/09/2003", "lucas.martin@example.com", "0400 100 007", "Tor007", "17/03/2026"),
    (PremiumMember, "Isla Thompson", "02/12/1985", "isla.thompson@example.com", "0400 100 008", "Tor008", "28/03/2026"),
    (NormalMember, "Oliver Davis", "16/04/1996", "oliver.davis@example.com", "0400 100 009", "Tor009", "09/04/2026"),
    (PremiumMember, "Grace Lee", "25/06/1989", "grace.lee@example.com", "0400 100 010", "Tor010", "20/04/2026"),
    (NormalMember, "Henry Walker", "08/02/1976", "henry.walker@example.com", "0400 100 011", "Tor011", "02/05/2026"),
    (PremiumMember, "Ella King", "13/10/2000", "ella.king@example.com", "0400 100 012", "Tor012", "15/05/2026"),
)


def seed_members(member_service: MemberService) -> None:
    members = []

    for member_data in SEED_MEMBERS:
        member_type, *member_details = member_data
        if member_service.get_member(member_details[4]) is None:
            members.append(member_type(*member_details))

    member_service.register_members(members)
