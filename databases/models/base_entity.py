from typing import Callable, NoReturn

from . import exceptions as exc, validators as val


class BaseEntity:
    _table_name: str
    _description: dict = {}
    _humans_names: dict = {}
    _human_prefix: str
    _BASE_VALIDATORS: dict[str, Callable[[str, str], NoReturn]] = {
        "required": val.check_required
    }

    @classmethod
    def create(cls) -> None:
        create_params: dict | None = cls._get_description_params("create")
        fields: list[str] = list(create_params.keys())
        values: dict = {}

        for field in fields:
            field_name: str = cls._humans_names.get(field, field)
            user_input: str = input(
                f"Введите {field_name} {cls._human_prefix}:"
            )

            cls._validate(create_params[field], user_input, field_name)

            values[field] = user_input

        print(values)

    @classmethod
    def _get_description_params(cls, params_name: str) -> dict:
        """
        Получение параметров из описания

        :param params_name: название параметра
        :return: параметры
        :exception: NoRequiredDescriptionParam - отсутствие параметра
        """
        params: dict | None = cls._description.get(params_name)

        if not params:
            raise exc.NoRequiredDescriptionParam(params_name)

        return params

    @staticmethod
    def _validate(
            field_params: dict, user_input: str, field_name: str
    ) -> None:
        validators: list[str] = field_params.get("validators") or []
        custom_validators: list[Callable[[str, str], None]] = \
            field_params.get("custom_validators") or []

        for custom_validator in custom_validators:
            custom_validator(user_input, field_name)

        for validator in validators:
            if validator in BaseEntity._BASE_VALIDATORS:
                BaseEntity._BASE_VALIDATORS[validator](
                    user_input, field_name
                )
