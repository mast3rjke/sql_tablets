"""Модуль работы с БД"""
import psycopg2
import databases.consts as consts
from . import sql_templates as sql_temp


def get_database_connection_url() -> str:
    """Получение адреса подключения к БД"""
    return f"postgresql://{consts.DB_USER}:{consts.DB_PASSWORD}@{consts.DB_HOST}:{consts.DB_PORT}/{consts.DB_NAME}"


db_connect = psycopg2.connect(get_database_connection_url())


def create_tables() -> None:
    """Создание базовых таблиц"""
    with db_connect.cursor() as db_cursor:
        for query in (
                sql_temp.CREATE_DIRECTORS_TABLE,
                sql_temp.CREATE_ACTORS_TABLE,
                sql_temp.CREATE_GENRES_TABLE,
                sql_temp.CREATE_FILMS_TABLE
        ):
            db_cursor.execute(query)

        db_connect.commit()
