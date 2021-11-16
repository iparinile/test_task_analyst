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
            often_category_name = logs_queries.get_category_which_often_bought_with_semi_manufactures(session)

            response = {
                "Category which is more often bought with semi_manufactures": often_category_name
            }
            return await self.make_response_json(body=response, status=200)
        elif report_number == 6:
            count_unpaid_carts = logs_queries.get_count_unpaid_carts(session)

            response = {
                "Unpaid carts": count_unpaid_carts
            }
            return await self.make_response_json(body=response, status=200)

        elif report_number == 7:
            count_users_with_repeat_pay = logs_queries.get_count_users_with_repeat_pay(session)

            response = {
                "Count_users_with_repeat_pay": count_users_with_repeat_pay
            }
            return await self.make_response_json(body=response, status=200)
        else:
            return await self.make_response_json(status=400, message='There is no such report number. '
                                                                     'Enter a number from 1 to 7')
