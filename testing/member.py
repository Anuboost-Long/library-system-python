class LibraryMemeber:
    def __init__(self, member_id, name):
        self.name = name
        self.id = member_id


member1 = LibraryMemeber(name="Kimlong ly", member_id="Torren001")
member2 = LibraryMemeber(name="Seth", member_id="Torren002")

print(
    vars(
        member1,
    ),
    vars(member2),
)
