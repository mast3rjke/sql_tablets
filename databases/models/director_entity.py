"""Модуль модели режиссера"""
from .base_entity import BaseEntity


class DirectorEntity(BaseEntity):
    """Модель режиссера"""
    _table_name: str = "directors"
    _humans_names: dict[str, str] = {
        "name": "имя",
        "country": "страну"
    }
    _human_prefix: str = "режиссера"
    _description: dict = {
        "fields": {
            "name": {"validators": ["required"]},
            "country": {"validators": ["required"]}
        }
    }
