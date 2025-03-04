"""Модуль модели жанра"""
from .base_entity import BaseEntity


class GenreEntity(BaseEntity):
    """Модель жанра"""
    _table_name: str = "genres"
    _description: dict = {
        "fields": {
            "name": {"validators": ["required"]}
        }
    }
    _humans_names: dict = {
        "name": "название"
    }
    _human_prefix: str = "жанра"
