from .base_entity import BaseEntity


class GenreEntity(BaseEntity):
    _table_name: str = "genres"
    _description: dict = {
        "create": {
            "name": {"validators": ["required"]}
        }
    }
    _humans_names: dict = {
        "name": "название"
    }
    _human_prefix: str = "жанра"


