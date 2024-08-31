import datetime
import random

from database.database import Database


class Table(Database):
    def __init__(self, name: str, **kwargs):
        self.name = name

        for title, field in kwargs.items():
            setattr(self, title, field)

        query: str = f"CREATE TABLE IF NOT EXISTS {self.name} ({', '.join([f'{field} {field_type.type}' for field, field_type in kwargs.items()])})"
        self.request(query, (), True)

    def select(self, fields: tuple, where: str = None, condition: any = None) -> any:
        query: str = f"SELECT {', '.join(fields) if len(fields) != 0 else '*'} FROM {self.name}"

        if where is not None:
            query += f""" WHERE {where} = {condition if type(condition).__name__ != 'str' else f"'{condition}'"}"""

        self.request(query, (), False)

        if len(fields) == 0:
            if where is None:
                return self.all()
            else:
                return self.one()
        elif len(fields) == 1:
            response = self.one()
            if response is not None:
                return response[0]
            else:
                return None
        else:
            return self.all()

    def order(self, fields: tuple, by: str, limit: int):
        query: str = f"SELECT {', '.join(fields) if len(fields) != 0 else '*'} FROM {self.name} ORDER BY {by} DESC LIMIT {limit}"
        self.request(query, (), False)

        if len(fields) == 0:
            return self.one()
        elif len(fields) == 1:
            response = self.one()
            if response is not None:
                return response[0]
            else:
                return None
        else:
            return self.all()

    def count(self, field: str = None) -> int:
        query: str = f"SELECT COUNT({'*' if field is None else field}) FROM {self.name}"
        self.request(query, (), False)
        response: tuple = self.one()
        return response[0]

    def insert(self, **kwargs) -> None:
        query: str = f"INSERT INTO {self.name} ({', '.join([field for field in kwargs.keys()])}) VALUES ({', '.join([f'%s' for _ in range(len(kwargs))])})"
        self.request(query, tuple(value for value in kwargs.values()), True)

    def delete(self, where: str, condition: any) -> None:
        query: str = f"DELETE FROM {self.name} WHERE {where} = %s"
        self.request(query, (condition, ), True)

    def assign(self, field: str, value: any, where: str, condition: any) -> None:
        query: str = f"UPDATE {self.name} SET {field} = %s WHERE {where} = %s"
        self.request(query, (value, condition), True)

    def increase(self, field: str, value: float, where: str, condition: any) -> None:
        query: str = f"UPDATE {self.name} SET {field} = {field} + %s WHERE {where} = %s"
        self.request(query, (value, condition), True)

    def decrease(self, field: str, value: float, where: str, condition: any) -> None:
        query: str = f"UPDATE {self.name} SET {field} = {field} - %s WHERE {where} = %s"
        self.request(query, (value, condition), True)


class UsersTable(Table):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self.start: float = 100
        self.referal: float = 50

    def user(self, userid: int):
        class User:
            def __init__(self, uid, user_id, username, language, wallet, balance, referals, last_code):
                self.uid: int = uid
                self.user_id: int = user_id
                self.username: str = username
                self.language: str = language
                self.wallet: str = wallet
                self.balance: float = balance
                self.referals: int = referals
                self.last_code: datetime.datetime = last_code

        data: tuple = self.select((), "user_id", userid)

        if data is None:
            return None

        _user: User = User(*data)

        return _user

    def rating(self, user_id: int) -> int:
        query: str = f"SELECT (SELECT COUNT(DISTINCT balance) + 1 FROM users WHERE balance > t1.balance) AS position FROM users AS t1 WHERE user_id = {user_id}"
        self.request(query, (), False)
        place: int = self.one()[0]
        return place


class MiningTable(Table):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self.booster: float = 1
        self.discount: float = 0

    def user(self, userid: int):
        class User:
            def __init__(self, user_id, username, last_claim, reactor, storage, bot, booster):
                self.user_id: int = user_id
                self.username: str = username
                self.last_claim: datetime.datetime = last_claim
                self.reactor: int = reactor
                self.storage: int = storage
                self.bot: float = bot
                self.booster: float = booster

        data: tuple = self.select((), "user_id", userid)

        if data is None:
            return None

        _user: User = User(*data)

        return _user

    def upgrade_price(self, device: str, level: int) -> float:
        if device == 'reactor':
            return int(150 * 2.2**(level-1) * (1 - self.discount))
        if device == 'storage':
            return int(75 * 2.2 ** (level - 1) * (1 - self.discount))


class CodesTable(Table):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)

    def generate(self, activations: int, value: float) -> str:
        symbols: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmopqrstuvwxyz0123456789"
        code: str = ""

        for s in range(16):
            code += random.choice(symbols)

        self.insert(code=code, value=value, activations=activations)
        return code

    def get(self) -> list:
        codes: list = self.select(())
        return codes

    def check(self, signature: str):
        class Code:
            def __init__(self, code, value, activations):
                self.code: int = code
                self.value: float = value
                self.activations: int = activations

        data: tuple = self.select((), "code", signature)

        try:
            _code: Code = Code(*data)
        except:
            return None

        return _code

    def activate(self, code) -> None:
        if code.activations == 1:
            self.delete("code", code.code)
        else:
            self.decrease("activations", 1, "code", code.code)
        return None


class Admin(Table):
    @classmethod
    def users(cls) -> int:
        query: str = f"SELECT COUNT(*) FROM users"
        cls.cursor.execute(query)
        return cls.cursor.fetchone()[0]

    @classmethod
    def miners(cls) -> int:
        query: str = f"SELECT COUNT(*) FROM mining"
        cls.cursor.execute(query)
        return cls.cursor.fetchone()[0]

    @classmethod
    def points(cls) -> float:
        query: str = f"SELECT SUM(balance) FROM users"
        cls.cursor.execute(query)
        return cls.cursor.fetchone()[0]

    @classmethod
    def codes(cls) -> int:
        query: str = f"SELECT COUNT(*) FROM codes"
        cls.cursor.execute(query)
        return cls.cursor.fetchone()[0]

    @classmethod
    def ids(cls) -> list:
        query: str = f"SELECT user_id FROM users"
        cls.cursor.execute(query)
        return [user[0] for user in cls.cursor.fetchall()]
