from borrow_operations import (
    AddBorrowedItem,
    DisplayProfile,
    ReportInvalidInput,
    ShutDownSystem,
    DisplayBorrowedItemByDueDate,
    DisplayReturnItemPanel,
    ViewBorrowedItems,
)
from display import DisplayOptions, PrintDivider, PrintSpace
from constants import options


def BorrowOperation(profile={}):
    selection_option = 0
    borrowed_items = []
    PrintSpace()
    while True:
        DisplayOptions(options)
        selection_option = input("Choose an option: ")

        if not selection_option.isnumeric():
            ReportInvalidInput()
            continue

        selection_option = int(selection_option)

        PrintSpace()
        PrintDivider("=")
        PrintSpace()

        if selection_option == 0:
            ShutDownSystem()
            break
        elif selection_option == 1:
            AddBorrowedItem(borrowed_items)
        elif selection_option == 2:
            ViewBorrowedItems(borrowed_items)
        elif selection_option == 3:
            DisplayBorrowedItemByDueDate(borrowed_items)
        elif selection_option == 4:
            DisplayReturnItemPanel(borrowed_items)
        elif selection_option == 5:
            DisplayProfile(profile)
