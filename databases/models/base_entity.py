"""Модуль базовой модели"""
from typing import Callable, NoReturn, List

from . import (
    exceptions as exc,
    validators as val,
    sql_templates as st
)


class BaseEntity:
    """Базовая модель"""
    _table_name: str
    _description: dict = {}
    # Человекочитаемые названия полей
    _humans_names: dict = {}
    # Человекочитаемое название сущности
    _human_prefix: str

    _DEFAULT_PRIMARY_KEY: str = "id"
    _BASE_VALIDATORS: dict[str, Callable[[str, str], NoReturn]] = {
        "required": val.check_required
    }

    @classmethod
    def create(cls, db_connect, db_cursor) -> None:
        """
        Создание записи с запросом и валидацией всех полей

        :param db_connect: подключение к БД
        :param db_cursor: курсор соединения с БД
        """
        fields_descriptions: dict | None = cls._get_description_params(
            "fields"
        )
        fields: list[str] = list(fields_descriptions.keys())
        values: dict = cls._get_fields_values(
            fields, fields_descriptions
        )
        fields_template, values_template = cls._get_template_vars(
            values
        )

        cls._query_execute(
            db_connect, db_cursor,
            st.CREATE_TEMPLATE,
            {
                "fields": ", ".join(fields_template),
                "values": f'({", ".join(values_template)})'
            },
            True
        )

    @classmethod
    def read(cls, _, db_cursor, entity_id=None) -> dict | None:
        """
        Чтение записи по первичному ключу

        :param _: подключение к БД
        :param db_cursor: курсор соединения с БД
        :param entity_id: идентификатор записи
        :return: запись из БД, None - если такого ключа нет
        """
        primary_field: dict = cls._get_description_params(
            "primary_key", True
        ) or cls._DEFAULT_PRIMARY_KEY
        entity_id: int = entity_id if entity_id else cls._get_entity_id()

        cls._query_execute(
            _, db_cursor,
            st.READ_TEMPLATE,
            {
                "primary_field": primary_field,
                "entity_id": entity_id
            }
        )
        data = db_cursor.fetchone()

        if not data:
            return data

        return cls._to_dict(data, db_cursor.description)

    @classmethod
    def list(cls, _, db_cursor) -> list[dict]:
        """
        Получение списка записей

        :param _: подключение к БД
        :param db_cursor: курсор соединения с БД
        :return: список записей
        """
        cls._query_execute(_, db_cursor, st.LIST_TEMPLATE, {})
        data = db_cursor.fetchall()

        if not data:
            return data

        return cls._to_list(data, db_cursor.description)

    @classmethod
    def delete(cls, db_connect, db_cursor) -> None:
        """
        Удаление записи по первичному ключу без проверки

        :param db_connect: подключение к БД
        :param db_cursor: курсор соединения с БД
        """
        primary_field: dict = cls._get_description_params(
            "primary_key", True
        ) or cls._DEFAULT_PRIMARY_KEY
        entity_id: int = cls._get_entity_id()

        cls._query_execute(
            db_connect, db_cursor,
            st.DELETE_TEMPLATE,
            {
                "primary_field": primary_field,
                "entity_id": entity_id
            },
            True
        )

    @classmethod
    def update(cls, db_connect, db_cursor):
        entity_id: int = cls._get_entity_id()
        primary_field: dict = cls._get_description_params(
            "primary_key", True
        ) or cls._DEFAULT_PRIMARY_KEY

        if not cls.read(db_connect, db_cursor, entity_id):
            raise exc.EntityNotFound(entity_id)

        fields_descriptions: dict | None = cls._get_description_params(
            "fields"
        )
        fields: list[str] = list(fields_descriptions.keys())
        values: dict = cls._get_fields_values(
            fields, fields_descriptions
        )

        fields_and_values = []

        for key, value in values.items():
            fields_and_values.append(
                f"\"{key}\" = '{value}'"
            )

        cls._query_execute(
            db_connect, db_cursor, st.UPDATE_TEMPLATE,
            {
                "entity_id": entity_id,
                "fields_and_values": ", ".join(fields_and_values),
                "primary_field": primary_field
            },
            True
        )

    @classmethod
    def _get_description_params(
            cls,
            params_name: str,
            skip_check: bool = False
    ) -> dict:
        """
        Получение параметров из описания

        :param params_name: название параметра
        :param skip_check: пропустить проверку
        :return: параметры
        :exception: NoRequiredDescriptionParam - отсутствие параметра
        """
        params: dict | None = cls._description.get(params_name)

        if not params and not skip_check:
            raise exc.NoRequiredDescriptionParam(params_name)

        return params or {}

    @classmethod
    def _get_fields_values(
            cls, fields: List[str], params: dict
    ) -> dict:
        """
        Получение значений по полям с валидацией

        :param fields: поля
        :param params: параметры полей
        :return: словарь вида название:значение
        """
        values: dict = {}

        for field in fields:
            field_name: str = cls._humans_names.get(field, field)
            user_input: str = input(
                f"Введите {field_name} {cls._human_prefix}:"
            )

            cls._validate(params[field], user_input, field_name)

            values[field] = user_input

        return values

    @staticmethod
    def _validate(
            field_params: dict, user_input: str, field_name: str
    ) -> None:
        """
        Валидация пользовательского ввода по описанию

        :param field_params: параметры поля
        :param user_input: пользовательский ввод
        :param field_name: человекочитаемое поле
        """
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

    @staticmethod
    def _get_template_vars(
            values: dict
    ) -> tuple[List[str], List[str]]:
        """
        Получение переменных шаблона

        :param values: карта значение и полей
        :return: форматированные списки полей и значений
        """
        fields_template: List[str] = []
        values_template: List[str] = []

        for key, value in values.items():
            fields_template.append(f'"{key}"')
            values_template.append(f"'{value}'")

        return fields_template, values_template

    @classmethod
    def _query_execute(
            cls, db_connect, db_cursor, template, params, need_commit=False
    ):
        """
        Выполнение запроса

        :param db_connect: подключение к БД
        :param db_cursor: курсор БД
        :param template: шаблон запроса
        :param params: доп. параметры запроса
        :param need_commit: закрытие транзакции по окончанию
        """
        query = template.format(
            table_name=cls._table_name,
            **params
        )

        db_cursor.execute(query)

        if need_commit:
            db_connect.commit()

    @classmethod
    def _get_entity_id(cls) -> int:
        """Получение идентификатора сущности от пользователя"""
        try:
            return int(input(
                f"Введите ИД {cls._human_prefix}: "
            ))
        except ValueError as ex:
            raise exc.StrIdNoParse() from ex

    @classmethod
    def _to_dict(cls, data, columns) -> dict:
        """
        Преобразование к словарю

        :param data: данные для преобразования
        :param columns: список колонок
        :return: словарь данных
        """
        new_data = {}

        for i in range(len(data)):
            new_data[columns[i].name] = data[i]

        return new_data

    @classmethod
    def _to_list(cls, data, columns) -> list:
        """
        Преобразование к списку

        :param data: данные для преобразования
        :param columns: список колонок
        :return: список словарей данных
        """
        new_data = []

        for row in data:
            new_data.append(cls._to_dict(row, columns))

        return new_data
