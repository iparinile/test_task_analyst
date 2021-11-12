from sqlalchemy import Integer, Column, ForeignKey

from db.models import BaseModel


class DBGoodsInCarts(BaseModel):
    __tablename__ = 'goods_in_carts'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    goods_id = Column(Integer, ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)
    cart_id = Column(Integer, ForeignKey('carts.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Integer, nullable=False)
