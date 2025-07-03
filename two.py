from datetime import datetime

from utils.shedulers.cleane_base_scheduler import get_first_day_next_month

# now_day = datetime.now().date()
# print(now_day)
# next_month = now_day.month + 1
# next_month = now_day.replace(day=1, month=next_month)
# print(type(next_month))
day = get_first_day_next_month()
print(day)
