from sqlalchemy import Integer, Column, DateTime, VARCHAR, ForeignKey

from db.models import BaseModel


class DBTransactions(BaseModel):
    __tablename__ = 'transactions'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_ip = Column(VARCHAR(255), ForeignKey('users.ip', ondelete='CASCADE'), nullable=False)
    datetime = Column(DateTime, nullable=False)
    type = Column(VARCHAR(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    goods_id = Column(Integer, ForeignKey('goods.id', ondelete='CASCADE'))
    cart_id = Column(Integer, ForeignKey('carts.id', ondelete='CASCADE'))
