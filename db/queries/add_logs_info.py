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


def create_user(session: DBSession, user_ip: str, user_id: int) -> None:
    new_user = DBUsers(
        ip=user_ip,
        id=user_id
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
        transaction_type: str,
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
