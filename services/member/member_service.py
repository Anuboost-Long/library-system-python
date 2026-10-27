from models.library_member import LibraryMember


class MemberService:
    def __init__(self):
        self.__members: dict[str, LibraryMember] = {}

    def register(self, member: LibraryMember) -> None:
        if member.member_id in self.__members:
            raise ValueError("Member already exists")

        self.__members[member.member_id] = member

    def get_member(self, member_id: str) -> LibraryMember | None:
        return self.__members.get(member_id)

    def get_all_members(self) -> list[LibraryMember]:
        return list(self.__members.values())
