import os

from sanic.request import Request
from sanic.response import BaseHTTPResponse

from db.database import DBSession
from db.exceptions import DBDataException, DBIntegrityException
from db.queries import logs as logs_queries
from helpers.parsing import parse_logs
from helpers.parsing.exception import ParseLogsException
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicLogsException, SanicDBException


class ParseLogsEndpoint(BaseEndpoint):
    async def method_get(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        logs_queries.clear_data(session)

        try:
            goods, users, carts, transactions = parse_logs(os.getenv("logs_file_name", "logs.txt"))
        except ParseLogsException as e:
            raise SanicLogsException(str(e))

        for user_ip in users.keys():
            user_id = users[user_ip]
            logs_queries.create_user(session, user_ip, user_id)

        for category_name in goods.keys():
            logs_queries.create_category(session, category_name)
            for goods_name in goods[category_name].keys():
                goods_id = goods[category_name][goods_name]
                category_id = logs_queries.get_category_id(session, category_name)
                logs_queries.create_goods(session, goods_id, category_id, goods_name)

        for cart_id in carts.keys():
            cart_info = carts[cart_id]
            logs_queries.create_cart(session, cart_id, cart_info['is_payed'])
            goods_in_cart = cart_info['goods']

            for goods_id in goods_in_cart.keys():
                amount = goods_in_cart[goods_id]
                logs_queries.create_goods_in_cart(session, cart_id, goods_id, amount)

        for user_ip in transactions.keys():
            transactions_list = transactions[user_ip]
            for transaction in transactions_list:
                try:
                    transaction_type = transaction['type']
                    if (transaction_type == 'cart') or (transaction_type == 'pay') or (
                            transaction_type == 'success_pay'):
                        logs_queries.create_transaction(
                            session,
                            user_ip=user_ip,
                            datetime_obj=transaction['date_time'],
                            transaction_type=transaction_type,
                            cart_id=transaction['cart_id']
                        )
                    else:
                        category_id = logs_queries.get_category_id(session, transaction['category_name'])
                        if transaction_type == 'select_category':
                            logs_queries.create_transaction(
                                session,
                                user_ip=user_ip,
                                datetime_obj=transaction['date_time'],
                                transaction_type=transaction_type,
                                category_id=category_id
                            )
                        elif transaction_type == 'select_goods':
                            goods_id = logs_queries.get_goods_id(session, category_id, transaction['goods_name'])
                            logs_queries.create_transaction(
                                session,
                                user_ip=user_ip,
                                datetime_obj=transaction['date_time'],
                                transaction_type=transaction_type,
                                category_id=category_id,
                                goods_id=goods_id
                            )

                except KeyError:
                    logs_queries.create_transaction(
                        session,
                        user_ip=user_ip,
                        datetime_obj=transaction['date_time']
                    )

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response = {
            "log_parsing_status": "added to the database"
        }
        return await self.make_response_json(body=response, status=201)
