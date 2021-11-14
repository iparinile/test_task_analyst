import datetime
from pprint import pprint

from helpers.parsing.exception import ParseLogsException


def parse_logs(path_to_logs: str) -> tuple:
    try:
        with open(path_to_logs, "r") as logs_file:
            lines = logs_file.readlines()
            users_id = dict()
            users_transactions = dict()
            goods = dict()
            carts = dict()

            for line in lines:
                transaction = dict()

                split_line = line.split()

                date_str = split_line[2]
                time_str = split_line[3]
                date_time_str = f"{date_str} {time_str}"
                date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                transaction["date_time"] = date_time_obj

                user_ip = split_line[6]
                if user_ip not in users_id.keys():
                    users_id[user_ip] = ''

                current_url = split_line[7]
                split_url = current_url.split('/')
                url_path = split_url[3:]
                url_path = [part_from_url for part_from_url in url_path if part_from_url != '']
                if len(url_path) > 0:
                    if url_path[0].startswith("cart"):
                        transaction["type"] = "cart"
                        cart_info = url_path[0].split("?")[1]
                        split_cart_info = cart_info.split("&")

                        cart_id = int(split_cart_info[2].split("=")[1])
                        transaction["cart_id"] = cart_id
                        goods_id = int(split_cart_info[0].split("=")[1])
                        transaction["goods_id"] = goods_id
                        amount = int(split_cart_info[1].split("=")[1])

                        # Поиск названия goods для текущего goods_id по последней транзакции с данного ip
                        last_transaction = users_transactions[user_ip][-1]
                        type_transaction = last_transaction['type']
                        if type_transaction == 'select_goods':
                            goods_name = last_transaction['goods_name']
                            category_name = last_transaction['category_name']
                            goods[category_name][goods_name] = goods_id
                        else:
                            raise ValueError

                        if cart_id not in carts.keys():
                            carts[cart_id] = {"goods": dict(), "is_payed": False}

                        carts[cart_id]["goods"][goods_id] = amount

                        # for counter_transaction
                    elif url_path[0].startswith("pay"):
                        transaction["type"] = "pay"
                        pay_info = url_path[0].split("?")[1]
                        split_pay_info = pay_info.split("&")

                        cart_id = int(split_pay_info[1].split("=")[1])
                        transaction["cart_id"] = cart_id
                        user_id = int(split_pay_info[0].split("=")[1])
                        transaction["user_id"] = user_id

                        if users_id[user_ip] == '':
                            users_id[user_ip] = user_id
                        elif users_id[user_ip] == user_id:
                            pass
                        else:
                            raise ValueError

                    elif url_path[0].startswith("success_pay"):
                        payed_cart_id = int(url_path[0].split("_")[2])
                        carts[payed_cart_id]["is_payed"] = True

                    else:
                        category_name = url_path[0]
                        transaction["category_name"] = category_name
                        if category_name not in goods.keys():
                            goods[category_name] = dict()

                        if len(url_path) == 2:
                            goods_name = url_path[1]
                            transaction["goods_name"] = goods_name
                            transaction['type'] = "select_goods"

                            if goods_name not in goods[category_name].keys():
                                goods[category_name][goods_name] = ''  # id
                        elif len(url_path) > 2:
                            raise ValueError
                        else:
                            transaction['type'] = "select_category"

                if user_ip not in users_transactions.keys():
                    users_transactions[user_ip] = [transaction]
                else:
                    users_transactions[user_ip].append(transaction)

            # pprint.pprint(users_transactions)
    except (ValueError, KeyError) as e:
        raise ParseLogsException(str(e))

    pprint(users_transactions)

    return goods, users_id, carts, users_transactions


# def get_country_by_ip(backend_users: list):
#     rs = (grequests.get(f"https://ipinfo.io/{ip}/json") for ip in backend_users)
#
#     print(grequests.map(rs))


if __name__ == '__main__':
    parse_logs("logs.txt")
