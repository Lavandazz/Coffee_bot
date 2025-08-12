from datetime import date

from utils.custom_calendar import MyCalendar

cal = MyCalendar(date(2025, 8, 11))  # Базовая дата — 11 августа 2025
august = cal.update_month_list()
print(len(cal.month_list))  # 31 (в августе 31 день)

# Перешли на следующий месяц
cal.day = date(2025, 9, 1)
cal.update_month_list()
print(len(cal.month_list))  # 30 (в сентябре 30 дней)