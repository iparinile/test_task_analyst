import os
from dotenv import load_dotenv

load_dotenv()


class SQLiteConfig:
    name = os.getenv('dbname', 'db.sqlite')
    url = rf'sqlite:///{name}'
