# Сколько не оплаченных корзин имеется
from sanic.request import Request
from sanic.response import BaseHTTPResponse

from db.database import DBSession
from db.queries import logs as logs_queries
from transport.sanic.endpoints import BaseEndpoint


class ReportEndpoint(BaseEndpoint):
    async def method_get(self, request: Request, body: dict, session: DBSession, report_number: int,
                         *args, **kwargs) -> BaseHTTPResponse:
        if report_number == 1:
            pass
        elif report_number == 2:
            pass
        elif report_number == 3:
            pass
        elif report_number == 4:
            pass
        elif report_number == 5:
            pass
        elif report_number == 6:
            count_unpaid_carts = logs_queries.get_count_unpaid_carts(session)

            response = {
                "Unpaid carts": count_unpaid_carts
            }
            return await self.make_response_json(body=response, status=200)

        elif report_number == 7:
            pass
        else:
            return await self.make_response_json(status=400, message='There is no such report number. '
                                                                     'Enter a number from 1 to 7')
