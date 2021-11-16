import datetime

from db.database import DBSession
from db.models import DBUsers, DBCategories, DBCarts, DBGoods, DBGoodsInCarts, DBTransactions


def clear_data(session: DBSession) -> None:
    session.delete_rows(DBUsers)
    session.delete_rows(DBCategories)
    session.delete_rows(DBCarts)
    session.delete_rows(DBGoods)
    session.delete_rows(DBGoodsInCarts)
    session.delete_rows(DBTransactions)


def create_user(session: DBSession, user_ip: str, user_id: int, user_country: str) -> None:
    new_user = DBUsers(
        ip=user_ip,
        id=user_id,
        country=user_country
    )

    session.add_model(new_user)


def create_category(session: DBSession, category_name: str) -> None:
    new_category = DBCategories(name=category_name)

    session.add_model(new_category)


def create_goods(session: DBSession, goods_id: int, category_id: int, goods_name: str) -> None:
    new_goods = DBGoods(
        id=goods_id,
        category_id=category_id,
        name=goods_name
    )

    session.add_model(new_goods)


def create_cart(session: DBSession, cart_id: int, is_payed: bool) -> None:
    new_cart = DBCarts(
        id=cart_id,
        is_payed=is_payed
    )

    session.add_model(new_cart)


def create_goods_in_cart(session: DBSession, cart_id: int, goods_id: int, amount: int) -> None:
    new_goods_in_cart = DBGoodsInCarts(
        goods_id=goods_id,
        cart_id=cart_id,
        amount=amount
    )

    session.add_model(new_goods_in_cart)


def create_transaction(
        session: DBSession,
        user_ip: str,
        datetime_obj: datetime.datetime,
        transaction_type: str = None,
        category_id: int = None,
        goods_id: int = None,
        cart_id: int = None
):
    new_transaction = DBTransactions(
        user_ip=user_ip,
        datetime=datetime_obj,
        type=transaction_type,
        category_id=category_id,
        goods_id=goods_id,
        cart_id=cart_id
    )

    session.add_model(new_transaction)


def get_category_id(session: DBSession, category_name: str) -> int:
    category = session.get_category_id_by_name(category_name)
    return category.id


def get_goods_id(session: DBSession, category_id: int, goods_name: str) -> int:
    goods = session.get_goods_id_by_name(goods_name, category_id)
    return goods.id


def get_count_unpaid_carts(session: DBSession) -> int:
    unpaid_carts = session.get_unpaid_carts()
    return unpaid_carts


def get_count_users_with_repeat_pay(session: DBSession) -> int:
    number_of_users = session.get_success_pay_transactions()
    return number_of_users


def get_country_with_max_count_transactions(session: DBSession) -> str:
    country_visits = dict()
    for user_ip, transaction_count in session.get_transactions_group_by_users():
        country = session.get_country_by_ip(user_ip).country
        if country is not None:  # По некоторым ip нет данных по стране
            if country not in country_visits.keys():
                country_visits[country] = transaction_count
            else:
                country_visits[country] += transaction_count
    return max(country_visits, key=country_visits.get)


def get_country_with_max_select_goods_in_fresh_fish(session: DBSession) -> str:
    country_visits = dict()
    fresh_fish_id = session.get_category_id_by_name('fresh_fish').id
    for user_ip, transaction_count in session.get_transactions_with_fresh_fish(fresh_fish_id):
        country = session.get_country_by_ip(user_ip).country
        if country is not None:
            if country not in country_visits.keys():
                country_visits[country] = transaction_count
            else:
                country_visits[country] += transaction_count
    return max(country_visits, key=country_visits.get)


def get_category_which_often_bought_with_semi_manufactures(session: DBSession) -> str:
    semi_manufactures_id = get_category_id(session, 'semi_manufactures')
    goods_in_semi_manufactures = []
    for goods in session.get_goods_in_semi_manufactures(semi_manufactures_id):
        goods_in_semi_manufactures.append(goods.id)

    categories_bought_with_semi_manufactures = dict()

    for cart in session.get_paid_carts():
        cart_id = cart.id
        for goods_in_carts in session.get_goods_in_cart_by_cart_id(cart_id):
            goods_id = goods_in_carts.goods_id
            if goods_id in goods_in_semi_manufactures:
                for goods in session.get_goods_in_cart_by_cart_id(cart_id):
                    category_id = session.get_category_id_by_goods_id(goods.goods_id).category_id
                    if category_id != semi_manufactures_id:
                        if category_id not in categories_bought_with_semi_manufactures.keys():
                            categories_bought_with_semi_manufactures[category_id] = 1
                        else:
                            categories_bought_with_semi_manufactures[category_id] += 1

    often_bought_with_semi_manufactures_category = max(categories_bought_with_semi_manufactures,
                                                       key=categories_bought_with_semi_manufactures.get)
    return session.get_category_name_by_category_id(often_bought_with_semi_manufactures_category).name


def get_part_of_day_when_max_visit_frozen_fish(session: DBSession) -> str:
    frozen_fish_id = get_category_id(session, 'frozen_fish')
    transactions_in_parts_of_day = {'night': 0, 'morning': 0, 'daytime': 0, 'evening': 0}
    for transaction in session.get_transactions_with_frozen_fish(frozen_fish_id):
        transaction_time = transaction.datetime.time()
        if datetime.time(0, 0, 0) <= transaction_time < datetime.time(5, 59, 59):
            transactions_in_parts_of_day['night'] += 1
        elif datetime.time(6, 0, 0) <= transaction_time < datetime.time(11, 59, 59):
            transactions_in_parts_of_day['morning'] += 1
        elif datetime.time(12, 0, 0) <= transaction_time < datetime.time(17, 59, 59):
            transactions_in_parts_of_day['daytime'] += 1
        elif datetime.time(18, 0, 0) <= transaction_time < datetime.time(23, 59, 59):
            transactions_in_parts_of_day['evening'] += 1
    return max(transactions_in_parts_of_day, key=transactions_in_parts_of_day.get)


def get_max_counter_transactions(session: DBSession) -> int:
    transactions_counter = dict()
    for hour_number in range(0, 24):
        transactions_counter[hour_number] = 0
    for transaction in session.get_all_transactions():
        transaction_time = transaction.datetime.time()
        for hour_number in transactions_counter.keys():
            if datetime.time(hour_number, 0, 0) <= transaction_time < datetime.time(hour_number, 59, 59):
                transactions_counter[hour_number] += 1
    return max(transactions_counter.values())
