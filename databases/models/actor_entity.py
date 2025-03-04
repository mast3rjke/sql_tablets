"""Модуль модели актера"""
from .director_entity import DirectorEntity


class ActorEntity(DirectorEntity):
    """Модель актера"""
    _table_name: str = "actors"
    _human_prefix: str = "актера"
