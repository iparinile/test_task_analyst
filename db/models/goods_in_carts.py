from sqlalchemy import Integer, Column

from db.models import BaseModel


class DBGoodsInCarts(BaseModel):
    __tablename__ = 'goods_in_carts'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    goods_id = Column(Integer, nullable=False)
    cart_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
