class NoRequiredDescriptionParam(RuntimeError):
    def __init__(self, params_name: str) -> None:
        super().__init__(
            f"В описании класса нет поля '{params_name}'"
        )


class NoRequiredField(ValueError):
    def __init__(self, field_name: str) -> None:
        super().__init__(
            f"Поле '{field_name}' обязательно для заполнения"
        )
