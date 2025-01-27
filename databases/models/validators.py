from typing import NoReturn
from . import exceptions as exc


def check_required(value: str, name: str) -> NoReturn:
    if not value:
        raise exc.NoRequiredField(name)
