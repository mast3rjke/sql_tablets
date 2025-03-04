"""Модуль констант БД"""
from enum import IntEnum

from . import models

DB_USER: str = "postgres"
DB_PASSWORD: str = "root"
DB_NAME: str = "db_films"
DB_HOST: str = "localhost"
DB_PORT: int = 5432


class OperationKey(IntEnum):
    """Перечисление базовых операций в модели"""
    CREATE = 1
    READ = 2
    LIST = 3
    UPDATE = 4
    DELETE = 5


OPERATIONS: dict[int, dict[str, str]] = {
    OperationKey.CREATE: {
        "human_name": "Создать",
        "method_name": "create"
    },
    OperationKey.READ: {
        "human_name": "Прочитать",
        "method_name": "read"
    },
    OperationKey.LIST: {
        "human_name": "Список",
        "method_name": "list"
    },
    OperationKey.UPDATE: {
        "human_name": "Обновить",
        "method_name": "update"
    },
    OperationKey.DELETE: {
        "human_name": "Удалить",
        "method_name": "delete"
    }
}

MODELS: dict[int, dict[str, str | models.BaseEntity]] = {
    1: {"human_name": "Жанр", "class": models.GenreEntity},
    2: {"human_name": "Актер", "class": models.ActorEntity},
    3: {"human_name": "Режиссер", "class": models.DirectorEntity}
}
