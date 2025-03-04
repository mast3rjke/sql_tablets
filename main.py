"""Основной модуль приложения"""
from databases.common import create_tables, db_connect
from databases import consts
from helpers import print_menu_and_get_id


if __name__ == "__main__":
    create_tables()

    operation_id: int = print_menu_and_get_id(
        "операцию",
        consts.OPERATIONS
    )
    model_id: int = print_menu_and_get_id(
        "сущность",
        consts.MODELS
    )

    method_name: str = consts.OPERATIONS[operation_id]["method_name"]
    class_obj = consts.MODELS[model_id]["class"]

    with db_connect.cursor() as db_cursor:
        result = getattr(class_obj, method_name)(db_connect, db_cursor)

        if result:
            print(result)

    db_connect.close()
