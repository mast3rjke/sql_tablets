"""Модуль валидаторов"""
from typing import NoReturn

from . import exceptions as exc


def check_required(value: str, name: str) -> NoReturn:
    """
    Валидация на обязательность значения

    :param value: пользовательское значение
    :param name: человекочитаемое название поля
    :exception: NoRequiredField - пустое поле
    """
    if not value:
        raise exc.NoRequiredField(name)
