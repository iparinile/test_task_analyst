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
            country = logs_queries.get_country_with_max_count_transactions(session)

            response = {
                "From this country most often visit the site": country
            }
            return await self.make_response_json(body=response, status=200)
        elif report_number == 2:
            country = logs_queries.get_country_with_max_select_goods_in_fresh_fish(session)

            response = {
                "From this country, they are most often interested in products "
                "from a certain category 'fresh_fish'": country
            }
            return await self.make_response_json(body=response, status=200)
        elif report_number == 3:
            part_day_name = logs_queries.get_part_of_day_when_max_visit_frozen_fish(session)

            response = {
                "At this time of day, the 'frozen_fish' category is most often viewed": part_day_name
            }
            return await self.make_response_json(body=response, status=200)
        elif report_number == 4:
            max_transaction_per_hour = logs_queries.get_max_counter_transactions(session)

            response = {
                "The maximum number of requests to the site per astronomical hour": max_transaction_per_hour
            }
            return await self.make_response_json(body=response, status=200)
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
