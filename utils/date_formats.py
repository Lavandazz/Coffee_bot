from datetime import date


def from_str_to_date_day(date_string: str) -> date:
    """Преобразование строки даты в формат date для дальнейшего использования в бд"""

    list_date = date_string.split('_')[1].split('.')
    print(list_date)
    call_date = list(map(int, list_date))
    print(call_date)
    return date(year=call_date[2], month=call_date[1], day=call_date[0])
