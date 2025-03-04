"""Модуль вспомогательных функций"""


def print_menu_and_get_id(prefix: str, menu_items: dict) -> int:
    """
    Вывод меню и получение идентификатора действия

    :param prefix: префикс выбираемой сущности
    :param menu_items: элементы меню
    :return: идентификатор действия
    """
    print(f"Выберете {prefix}:")

    for item_key, item_data in menu_items.items():
        print(f"{item_key}. {item_data.get('human_name')}")

    menu_item_id: str = input()

    if (
            not menu_item_id.isdigit()
            or int(menu_item_id) not in menu_items
    ):
        raise ValueError("Неправильный ввод")

    return int(menu_item_id)
