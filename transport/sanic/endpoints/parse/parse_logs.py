import os
from pprint import pprint

from sanic.request import Request
from sanic.response import BaseHTTPResponse

from db.database import DBSession
from db.queries.add_logs_info import create_user
from helpers.parsing import parse_logs
from helpers.parsing.exception import ParseLogsException
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicLogsException


class ParseLogsEndpoint(BaseEndpoint):
    async def method_get(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        try:
            goods, users, carts, users_transactions = parse_logs(os.getenv("logs_file_name", "logs.txt"))
        except ParseLogsException as e:
            raise SanicLogsException(str(e))

        pprint(goods)
        pprint(carts)
        pprint(users)

        for user_ip in users.keys():
            user_id = users[user_ip]
            create_user(session, user_ip, user_id)
        response = {
            "log_parsing_status": "added to the database"
        }
        return await self.make_response_json(body=response, status=200)
