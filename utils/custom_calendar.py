import calendar
from datetime import date, timedelta
from utils.logging_config import bot_logger


month_names = {
                1: "январь", 2: "февраль", 3: "март",
                4: "апрель", 5: "май", 6: "июнь",
                7: "июль", 8: "август", 9: "сентябрь",
                10: "октябрь", 11: "ноябрь", 12: "декабрь"
            }


class MyCalendar:
    """
    Класс для работы с календарными данными.

    Хранит текущую дату и предоставляет методы для получения
    списка дней текущего, следующего и предыдущего месяцев.
    Также содержит метод для получения названия месяца на русском языке.
    """

    def __init__(self, day: date = date.today()):
        """
        Инициализация календаря.

        :param day: Дата, относительно которой будет строиться календарь.
                    По умолчанию используется текущая дата.
        """
        self.day = day
        self.month_list = []

    @classmethod
    def get_month_name(cls, day: date) -> str:
        """
        Возвращает название месяца на русском языке.

        :param day: Объект datetime.date.
        :return: Название месяца, например, "Январь".
        """
        return month_names.get(day.month, "")

    @classmethod
    def current_date_list(cls, day: date) -> list:
        """
        Формирует список всех дней текущего месяца.

        :param day: Объект datetime.date, по которому определяется месяц.
        :return: Список объектов datetime.date для каждого дня месяца.
        """
        first_day = day.replace(day=1)
        _, last_day = calendar.monthrange(day.year, day.month)
        return [first_day + timedelta(days=i) for i in range(last_day)]

    @classmethod
    def next_date_list(cls, day: date) -> list:
        """
        Формирует список всех дней следующего месяца.

        Автоматически учитывает переход на новый год, если текущий месяц — декабрь.

        :param day: Объект datetime.date, по которому определяется следующий месяц.
        :return: Список объектов datetime.date для каждого дня следующего месяца.
        """
        if day.month == 12:
            next_month = date(day.year + 1, 1, 1)
        else:
            next_month = date(day.year, day.month + 1, 1)
        return cls.current_date_list(next_month)

    @classmethod
    def early_date_list(cls, day: date) -> list:
        """
        Формирует список всех дней предыдущего месяца.

        Автоматически учитывает переход на предыдущий год, если текущий месяц — январь.

        :param day: Объект datetime.date, по которому определяется предыдущий месяц.
        :return: Список объектов datetime.date для каждого дня предыдущего месяца.
        """
        if day.month == 1:
            prev_month = date(day.year - 1, 12, 1)
        else:
            prev_month = date(day.year, day.month - 1, 1)
        return cls.current_date_list(prev_month)

    def update_month_list(self):
        """
        Обновляет список month_list для текущего экземпляра календаря.

        month_list будет содержать объекты datetime.date для каждого дня
        текущего месяца, относительно даты self.day.
        """
        self.month_list = self.current_date_list(self.day)

