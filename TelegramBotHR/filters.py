from typing import Union, Dict, Any
import db
from aiogram.filters import BaseFilter
from aiogram.types import Message

'''
    Файл с дополнительными фильтрами
'''


class AdminRoleFilter(BaseFilter):
    '''
    Фильтр для определения администратора
    '''

    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        tg_id = message.from_user.id
        return db.check_admin_role(tg_id)


class UserRoleFilter(BaseFilter):
    '''
    Фильтр для определения обычного пользователя
    '''

    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        tg_id = message.from_user.id
        return db.check_user_role(tg_id)
