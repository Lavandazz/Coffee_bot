from datetime import date
import re
d = '23. 07, 2025'

# day_1 = map(int, d.replace(' ', '').split('.'))
#
# day, month, year = day_1
# date_1 = date(year, month, day)
#
# print(date_1)


def return_date_from_str(date_string):
        text = re.sub(r'[-.,: ]', ' ', date_string).split()
        day, month, year = map(int, text)
        obj_date = date(year, month, day)
        print(obj_date)
return_date_from_str(d)
