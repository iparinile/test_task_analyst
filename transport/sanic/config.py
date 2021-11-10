import os
from dotenv import load_dotenv

load_dotenv()


class SanicConfig:

    host = os.getenv('host', 'localhost')
    port = int(os.getenv('port', 8000))
    workers = int(os.getenv('workers', 1))
    debug = bool(os.getenv('debug', False))
