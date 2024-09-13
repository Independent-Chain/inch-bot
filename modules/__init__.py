from aiogram import Router

class ModulesManager:
    def __init__(self, name: str):
        self.name = name
        self.router = Router()
        self.modules = dict()

    def connect(self, path: str, name: str) -> None:
        module = __import__(f"{path}.{name}", fromlist=[""])
        self.modules[name] = module
        return None

    def disconnect(self, name: str) -> None:
        del self.modules[name]
        return None
