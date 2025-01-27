from databases.common import create_tables, db_connect, create_genre, create_director
from databases.models.genre_entity import GenreEntity


if __name__ == "__main__":
    create_tables()

    user_input: str = input("""Выберете операцию:
    1. Создать жанр
    2. Создать режисcера
    """)

    if not user_input.isdigit() or int(user_input) not in (1, 2):
        raise ValueError("Неправильный ввод")

    match int(user_input):
        case 1:
            GenreEntity.create()
        case 2:
            create_director()

    db_connect.close()
