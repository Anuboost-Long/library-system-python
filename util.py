from constants import max_date
import time


def CheckDateValidity(date: str):
    date_array = date.split("/")

    if len(date_array) != 3:
        print("Invalid date. Use the DD/MM/YYYY format.")
        return False

    day = date_array[0]
    month = date_array[1]
    year = date_array[2]

    if len(day) != 2 or len(month) != 2 or len(year) != 4:
        print("Invalid date. Use the DD/MM/YYYY format.")
        return False

    if not day.isnumeric() or not month.isnumeric() or not year.isnumeric():
        print("Invalid date. Enter a valid calendar date.")
        return False

    day_int = int(day)
    month_int = int(month)
    year_int = int(year)

    if month_int < 1 or month_int > 12:
        print("Invalid date. Enter a valid calendar date.")
        return False

    if max_date[month_int] < day_int or day_int < 1:
        print("Invalid date. Enter a valid calendar date.")
        return False

    is_leap_year = is_leap_year = year_int % 400 == 0 or (
        year_int % 4 == 0 and year_int % 100 != 0
    )

    if not is_leap_year and month_int == 2 and day_int > 28:
        print("Invalid date. Enter a valid calendar date.")
        return False

    return True


def GroupItemByField(item_list: list, field: str):
    item_groups = {}
    list_index = 0
    while list_index < len(item_list):

        current_item = item_list[list_index]
        current_field = current_item[field]

        if not item_groups.get(current_field):
            item_groups[current_field] = []

        item_groups[current_field].append(current_item)
        list_index += 1
    return item_groups


def GetCurrentDateWithFormat(format="%d/%m/%Y"):
    return time.strftime(format)
