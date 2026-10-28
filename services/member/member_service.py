from models.library_member import LibraryMember


class MemberService:
    def __init__(self):
        self.__members: dict[str, LibraryMember] = {}

    def register(self, member: LibraryMember) -> None:
        if member.member_id in self.__members:
            raise ValueError("Member already exists")

        self.__members[member.member_id] = member

    def register_members(self, members: list[LibraryMember]) -> None:
        member_ids = [member.member_id for member in members]

        if len(member_ids) != len(set(member_ids)) or any(
            member_id in self.__members for member_id in member_ids
        ):
            raise ValueError("Member already exists")

        self.__members.update({member.member_id: member for member in members})

    def get_member(self, member_id: str) -> LibraryMember | None:
        return self.__members.get(member_id)

    def get_all_members(self) -> list[LibraryMember]:
        return list(self.__members.values())

    def get_members(self, offset: int, limit: int) -> list[LibraryMember]:
        if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0:
            raise ValueError("Offset must be a non-negative integer")

        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError("Limit must be a positive integer")

        return list(self.__members.values())[offset : offset + limit]
