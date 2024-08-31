from mysql.connector import connect
from core.secrets import DATABASE


class Database:
    host = DATABASE["host"]
    username = DATABASE["username"]
    password = DATABASE["password"]
    scheme = DATABASE["scheme"]

    connection = connect(host=host, user=username, password=password, database=scheme)
    cursor = connection.cursor()

    def request(self, query: str, values: tuple, commit: bool) -> None:
        self.cursor.execute(query, values)
        if commit:
            self.connection.commit()

    def one(self) -> tuple:
        response: tuple = self.cursor.fetchone()
        return response

    def all(self) -> list:
        response: list = self.cursor.fetchall()
        return response