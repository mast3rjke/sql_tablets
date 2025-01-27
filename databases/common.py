import psycopg2
import databases.consts as consts
from . import sql_templates as sql_temp


def get_database_connection_url() -> str:
    return f"postgresql://{consts.DB_USER}:{consts.DB_PASSWORD}@{consts.DB_HOST}:{consts.DB_PORT}/{consts.DB_NAME}"


db_connect = psycopg2.connect(get_database_connection_url())


def create_tables() -> None:
    with db_connect.cursor() as db_cursor:
        for query in (
                sql_temp.CREATE_DIRECTORS_TABLE,
                sql_temp.CREATE_ACTORS_TABLE,
                sql_temp.CREATE_GENRES_TABLE,
                sql_temp.CREATE_FILMS_TABLE
        ):
            db_cursor.execute(query)

        db_connect.commit()


def create_genre() -> None:
    name: str = input("Введите название жанра:")

    if not name:
        raise ValueError("Название жанра не может быть пустым!")

    with db_connect.cursor() as db_cursor:
        db_cursor.execute(f"""
            INSERT INTO "genres"("name") VALUES ('{name}')
        """)
        db_connect.commit()


def create_director() -> None:
    name: str = input("Введите имя режиссера:")
    country: str = input("Введите страну режиссера:")

    if not name:
        raise ValueError("Имя режиссера не может быть пустым!")

    if not country:
        raise ValueError("Страна режиссера не может быть пустым!")

    with db_connect.cursor() as db_cursor:
        db_cursor.execute(f"""
            INSERT INTO 
                "directors"("name", "country") 
            VALUES 
                ('{name}', '{country}')
        """)
        db_connect.commit()
