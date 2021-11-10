from transport.sanic.config import SanicConfig
from db.config import SQLiteConfig


class ApplicationConfig:
    sanic: SanicConfig
    database: SQLiteConfig

    def __init__(self):
        self.sanic = SanicConfig()
        self.database = SQLiteConfig()
