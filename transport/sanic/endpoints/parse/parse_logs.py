import os
from pprint import pprint

from sanic.request import Request
from sanic.response import BaseHTTPResponse

from db.database import DBSession
from db.exceptions import DBDataException, DBIntegrityException
from db.queries.add_logs_info import create_user, clear_data, create_category, create_goods, create_cart, \
    create_goods_in_cart, get_category_id, create_transaction
from helpers.parsing import parse_logs
from helpers.parsing.exception import ParseLogsException
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicLogsException, SanicDBException


class ParseLogsEndpoint(BaseEndpoint):
    async def method_get(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        clear_data(session)

        try:
            goods, users, carts, transactions = parse_logs(os.getenv("logs_file_name", "logs.txt"))
        except ParseLogsException as e:
            raise SanicLogsException(str(e))

        for user_ip in users.keys():
            user_id = users[user_ip]
            create_user(session, user_ip, user_id)

        for category_name in goods.keys():
            create_category(session, category_name)
            for goods_name in goods[category_name].keys():
                goods_id = goods[category_name][goods_name]
                category_id = get_category_id(session, category_name)
                create_goods(session, goods_id, category_id, goods_name)

        for cart_id in carts.keys():
            cart_info = carts[cart_id]
            create_cart(session, cart_id, cart_info['is_payed'])
            goods_in_cart = cart_info['goods']

            for goods_id in goods_in_cart.keys():
                amount = goods_in_cart[goods_id]
                create_goods_in_cart(session, cart_id, goods_id, amount)

        for user_ip in transactions.keys():
            transactions_list = transactions[user_ip]
            for transaction in transactions_list:
                try:
                    transaction_type = transaction['type']
                    if transaction_type == 'select_category':
                        category_id = get_category_id(session, transaction['category_name'])
                        create_transaction(
                            session,
                            user_ip=user_ip,
                            datetime_obj=transaction['date_time'],
                            transaction_type=transaction_type,
                            category_id=category_id
                        )

                except KeyError:
                    pass

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response = {
            "log_parsing_status": "added to the database"
        }
        return await self.make_response_json(body=response, status=200)
