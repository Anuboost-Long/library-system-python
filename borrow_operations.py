from display import PrintDivider, PrintInformation, PrintSpace
from util import CheckDateValidity, GroupItemByField, GetCurrentDateWithFormat


def ReportInvalidInput():
    print("Invalid selection. Choose a number from the menu.")
    PrintSpace()
    PrintDivider("=")
    PrintSpace()


def ShutDownSystem():
    print("Borrow tracker closed.")


def AddBorrowedItem(borrowed_items: list):
    item = {
        "id": len(borrowed_items) + 1,
        "name": input("Item name: "),
        "due_date": "",
        "is_returned": False,
        "return_date": None,
    }

    while True:
        PrintSpace()
        item["due_date"] = input("Due date (DD/MM/YYYY): ")
        if CheckDateValidity(item["due_date"]):
            borrowed_items.append(item)
            break

    PrintSpace()
    PrintDivider("=")
    PrintSpace()


def DisplayBorrowedItems(borrowed_items: list):
    print("BORROWED ITEMS")
    PrintDivider("-")
    item_index = 0
    while item_index < len(borrowed_items):
        item = borrowed_items[item_index]
        status = "Returned" if item["is_returned"] else "Borrowed"
        print(f"{item_index + 1}. {item['name']}")
        print(f"   Due date    : {item['due_date']}")
        print(f"   Status      : {status}")
        print(f"   Return date : {item['return_date']}")
        print()
        item_index += 1
    PrintDivider("=")
    PrintSpace()


def ViewBorrowedItems(borrowed_items: list):
    DisplayBorrowedItems(borrowed_items)
    input("Press Enter to return to the menu: ")
    print("Returning to the menu...")
    PrintSpace()


def DisplayBorrowedItemByDueDate(borrowed_items: list):
    item_groups = GroupItemByField(borrowed_items, "due_date")
    group_keys = list(item_groups.keys())

    group_index = 0
    while group_index < len(group_keys):

        group_key = group_keys[group_index]
        grouped_item_list = item_groups[group_key]

        print(f"DUE DATE: {group_key}")

        PrintSpace()
        PrintDivider("=")
        PrintSpace()

        group_index += 1
        DisplayBorrowedItems(grouped_item_list)

    input("Press Enter to return to the menu: ")
    print("Returning to the menu...")


def DisplayReturnItemPanel(borrowed_items: list):
    while True:
        print("MARK AN ITEM AS RETURNED")

        PrintSpace()
        PrintDivider("=")
        PrintSpace()

        DisplayBorrowedItems(borrowed_items)
        print("  [0] Return to the menu")

        selection = input("Choose an item: ")

        if not selection.isnumeric():
            ReportInvalidInput()
            continue

        selection = int(selection)

        if selection == 0:
            print("Returning to the menu...")
            break

        if selection > len(borrowed_items) or selection < 0:
            ReportInvalidInput()
            PrintSpace()
            PrintDivider("=")
            PrintSpace()
            continue

        item = borrowed_items[selection - 1]

        item["is_returned"] = True
        item["return_date"] = GetCurrentDateWithFormat()


def DisplayProfile(profile: dict):
    PrintInformation(profile)
    input("Press Enter to return to the menu: ")
    print("Returning to the menu...")
    PrintSpace()
