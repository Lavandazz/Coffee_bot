from typing import Optional, Dict, List
from datetime import datetime

class MockHoroscope:
    @staticmethod
    def get_mock_data(current_month) -> List[Dict]:
        return [
            {
                "id": 1,
                "zodiac": "Овен",
                "month": current_month,
                "text": "Гуща сложилась в образ меча, но лезвие притуплено... Ветер перемен дует в ваши паруса, но спешка может обернуться потерей."
            },
            {
                "id": 2,
                "zodiac": "Телец",
                "month": current_month,
                "text": "На дне чаши — золотая монета, но она покрыта паутиной... Финансовый поток замедлится, но не иссякнет."
            },
            {
                "id": 3,
                "zodiac": "Близнецы",
                "month": current_month,
                "text": "Две тени в чаше танцуют, но не могут коснуться друг друга... Вам будет трудно выбрать между разумом и сердцем."
            },
            {
                "id": 4,
                "zodiac": "Рак",
                "month": current_month,
                "text": "Луна в вашей чаше утонула, но не погасла... Месяц начнется с тоски по чему-то утраченному."
            },
            {
                "id": 5,
                "zodiac": "Лев",
                "month": current_month,
                "text": "Корона в гуще, но она из хрупкого песка... Вас ждет испытание тщеславием."
            },
            {
                "id": 6,
                "zodiac": "Дева",
                "month": current_month,
                "text": "Чаша показывает замок с потерянным ключом... Вы зациклены на деталях, но ответ лежит в простом."
            },
            {
                "id": 7,
                "zodiac": "Весы",
                "month": current_month,
                "text": "Весы качаются, но на одной чаше — перо, на другой — камень... Вам предстоит трудный выбор."
            },
            {
                "id": 8,
                "zodiac": "Скорпион",
                "month": current_month,
                "text": "В гуще — змея, кусающая собственный хвост... Ваша страсть может обернуться саморазрушением."
            },
            {
                "id": 9,
                "zodiac": "Стрелец",
                "month": current_month,
                "text": "Стрела летит к солнцу, но не сгорает... Вас ждет путешествие — не обязательно вдаль."
            },
            {
                "id": 10,
                "zodiac": "Козерог",
                "month": current_month,
                "text": "Гора в чаше, но тропа ведет в обход... Вы упрямо лезете вверх, но судьба готовит вам боковой путь."
            },
            {
                "id": 11,
                "zodiac": "Водолей",
                "month": current_month,
                "text": "Вода в чаше бурлит, но не выплескивается... Ваши идеи опережают время, но мир еще не готов."
            },
            {
                "id": 12,
                "zodiac": "Рыбы",
                "month": current_month,
                "text": "Рыбы в чаше плывут против течения... Вы чувствуете, что реальность — лишь сон?"
            }
        ]

    @staticmethod
    async def get_or_none(zodiac: str, month: str) -> Optional[Dict]:
        for item in MockHoroscope.get_mock_data(month):
            if item["zodiac"] == zodiac and item["month"] == month:
                return None
                # return item
        return None
