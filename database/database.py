from mysql.connector import connect
from config.config import Config, load_config


class Database:
    config: Config = load_config()

    host = config.db.host
    username = config.db.username
    password = config.db.password
    scheme = config.db.scheme

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