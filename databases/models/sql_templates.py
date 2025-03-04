"""Модуль шаблонов SQL"""

CREATE_TEMPLATE: str = """
    INSERT INTO 
        "{table_name}"({fields})
    VALUES
        {values}
"""

READ_TEMPLATE: str = """
    SELECT
        *
    FROM
        "{table_name}"
    WHERE 
        "{primary_field}" = {entity_id}
"""

LIST_TEMPLATE: str = """
    SELECT
        *
    FROM
        "{table_name}"
"""

DELETE_TEMPLATE: str = """
    DELETE
    FROM
        "{table_name}"
    WHERE 
        "{primary_field}" = {entity_id}
"""

UPDATE_TEMPLATE: str = """
    UPDATE
        "{table_name}"
    SET
        {fields_and_values}
    WHERE 
        "{primary_field}" = {entity_id}
"""
