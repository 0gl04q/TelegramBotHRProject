import db
from aiogram.filters import BaseFilter
from aiogram.types import Message
import languages.languages as lg

'''
    Файл с дополнительными фильтрами
'''


class AdminRoleFilter(BaseFilter):
    """
    Фильтр для определения администратора
    """

    async def __call__(self, message: Message) -> bool:
        tg_id = message.from_user.id

        return db.check_admin_role(tg_id)


class UserRoleFilter(BaseFilter):
    """
    Фильтр для определения обычного пользователя
    """

    async def __call__(self, message: Message) -> bool:
        tg_id = message.from_user.id
        return db.check_user_role(tg_id)


class CheckSurveysFilter(BaseFilter):
    """
    Фильтр для кнопки проверки наличия опросов
    """

    async def __call__(self, message: Message) -> bool:
        tg_id = message.from_user.id
        language = db.get_language(tg_id)
        language_data = lg.get_languages_data()
        answer = language_data[language]['UserWorks']['Keyboards']['CheckSurveys']
        return message.text == answer


class ChangeLanguageFilter(BaseFilter):
    """
    Фильтр для кнопки смены языка
    """

    async def __call__(self, message: Message) -> bool:
        tg_id = message.from_user.id
        language = db.get_language(tg_id)
        language_data = lg.get_languages_data()
        answer = language_data[language]['UserWorks']['Keyboards']['SelectLanguage']
        return message.text == answer

