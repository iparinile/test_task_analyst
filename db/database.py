from typing import List

from sqlalchemy import func
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker, Session, Query

from db.exceptions import DBIntegrityException, DBDataException
from db.models import BaseModel, DBBackendUsers, DBCategories, DBGoods, DBCarts, DBTransactions, DBGoodsInCarts, DBUsers


class DBSession:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *args, **kwargs) -> Query:
        return self._session.query(*args, **kwargs)

    def delete_rows(self, model) -> Query:
        return self.query(model).delete()

    def users(self) -> Query:
        return self.query(DBBackendUsers).filter(DBBackendUsers.is_delete == 0)

    def close_session(self):
        self._session.close()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

    def get_backend_user_by_login(self, login: str) -> DBBackendUsers:
        return self.users().filter(DBBackendUsers.login == login).first()

    def get_backend_user_by_id(self, uid: int) -> DBBackendUsers:
        return self.users().filter(DBBackendUsers.id == uid).first()

    def get_user_all(self) -> List['DBBackendUsers']:
        qs = self.users()
        # print(qs)
        return qs.all()

    def get_category_id_by_name(self, category_name: str) -> DBCategories:
        return self.query(DBCategories).filter(DBCategories.name == category_name).first()

    def get_goods_id_by_name(self, goods_name: str, category_id: int) -> DBGoods:
        return self.query(DBGoods).filter(DBGoods.category_id == category_id, DBGoods.name == goods_name).first()

    def get_success_pay_transactions(self) -> int:
        qs = self.query(func.count(DBTransactions.id), DBTransactions.user_ip) \
            .filter(DBTransactions.type == 'success_pay').group_by(DBTransactions.user_ip) \
            .having(func.count(DBTransactions.id) > 1)
        return qs.count()

    def get_transactions_group_by_users(self) -> List[DBTransactions]:
        return self.query(DBTransactions.user_ip, func.count(DBTransactions.id)).group_by(DBTransactions.user_ip)

    def get_transactions_with_fresh_fish(self, fresh_fish_id: int) -> List[DBTransactions]:
        return self.query(DBTransactions.user_ip, func.count(DBTransactions.id)) \
            .filter(DBTransactions.category_id == fresh_fish_id, DBTransactions.type == 'select_goods') \
            .group_by(DBTransactions.user_ip)

    def get_country_by_ip(self, user_ip: str) -> DBUsers:
        return self.query(DBUsers.country).filter(DBUsers.ip == user_ip).first()

    def get_paid_carts(self) -> List[DBCarts]:
        qs = self.query(DBCarts.id).filter(DBCarts.is_payed == True)
        return qs.all()

    def get_goods_in_cart_by_cart_id(self, cart_id: int) -> List[DBGoodsInCarts]:
        return self.query(DBGoodsInCarts.goods_id).filter(DBGoodsInCarts.cart_id == cart_id).all()

    def get_goods_in_semi_manufactures(self, semi_manufactures_id: int) -> List[DBGoods]:
        return self.query(DBGoods.id).filter(DBGoods.category_id == semi_manufactures_id).all()

    def get_category_id_by_goods_id(self, goods_id: int) -> DBGoods:
        return self.query(DBGoods.category_id).filter(DBGoods.id == goods_id).first()

    def get_category_name_by_category_id(self, category_id: int) -> DBCategories:
        return self.query(DBCategories.name).filter(DBCategories.id == category_id).first()

    def get_unpaid_carts(self) -> int:
        qs = self.query(DBCarts).filter(DBCarts.is_payed == False)
        return qs.count()

    def get_transactions_with_frozen_fish(self, frozen_fish_id: int) -> List[DBTransactions]:
        return self.query(DBTransactions.id, DBTransactions.datetime) \
            .filter(DBTransactions.category_id == frozen_fish_id, DBTransactions.type == 'select_category')

    def get_all_transactions(self) -> List[DBTransactions]:
        return self.query(DBTransactions.id, DBTransactions.datetime).all()

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

        if need_close:
            self.close_session()


class DataBase:
    connexion: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'

    def __init__(self, connection: Engine):
        self.connexion = connection
        self.session_factory = sessionmaker(bind=self.connexion)

    def check_connection(self):
        self.connexion.execute(self._test_query).fetchone()

    def make_session(self) -> DBSession:
        session = self.session_factory()
        return DBSession(session)
