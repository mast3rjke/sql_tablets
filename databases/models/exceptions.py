"""Модуль исключений"""


class NoRequiredDescriptionParam(RuntimeError):
    """Класс-исключение при отсутствии параметра в описании модели"""
    def __init__(self, params_name: str) -> None:
        super().__init__(
            f"В описании класса нет поля '{params_name}'"
        )


class NoRequiredField(ValueError):
    """
    Класс-исключение при отсутствии
    обязательного поля пользовательского ввода
    """
    def __init__(self, field_name: str) -> None:
        super().__init__(
            f"Поле '{field_name}' обязательно для заполнения"
        )


class StrIdNoParse(ValueError):
    """Класс-исключение при переводе пользовательской строки в число"""
    def __init__(self) -> None:
        super().__init__(
            "ИД невозможно преобразовать к числу"
        )


class EntityNotFound(KeyError):
    """Класс-исключение при отсутствии записи по ключу"""
    def __init__(self, entity_id: int) -> None:
        super().__init__(f"Нет данных по ключу \"{entity_id}\"")

