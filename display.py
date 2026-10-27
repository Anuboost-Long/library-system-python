from util import CheckDateValidity


DISPLAY_WIDTH = 52


def PrintDivider(character: str = "-"):
    print(character * DISPLAY_WIDTH)


def PrintSpace():
    print()


def DisplayHeader():
    PrintDivider("=")
    print("              PERSONAL BORROW TRACKER")
    PrintDivider("=")
    PrintSpace()


def PrintWelcome(profile: dict):
    print(f"Welcome, {profile['name']}.")
    PrintSpace()
    PrintInformation(profile)


def PrintInformation(profile: dict):
    print("PROFILE")
    PrintDivider("-")
    print(f"Name        : {profile['name']}")
    print(f"Date of birth: {profile['dob']}")
    print(f"Email       : {profile['email']}")
    print(f"Phone       : {profile['mobile']}")
    PrintSpace()
    PrintDivider("=")


def GetInfo():
    name = input("Name: ")

    while True:
        dob = input("Date of birth (DD/MM/YYYY): ")
        if CheckDateValidity(dob):
            break

    return {
        "name": name,
        "dob": dob,
        "email": input("Email: "),
        "mobile": input("Phone number: "),
    }


def DisplayOptions(options: list):
    print("MENU")
    PrintDivider("-")
    index = 0
    while index < len(options):
        print(f"  [{options[index]['id']}] {options[index]['name']}")
        index += 1

    PrintSpace()
    PrintDivider("=")
    PrintSpace()
