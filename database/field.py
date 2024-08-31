from database.database import Database


class Field(Database):
    def __init__(self, name: str, field_type: str, parameters: str = None, table: str = None):
        self.name = name
        self.type = field_type
        self.table = table

        if parameters:
            self.type += f" {parameters}"
