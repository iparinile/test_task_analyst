from sqlalchemy import Integer, Column, DateTime, VARCHAR

from db.models import BaseModel


class DBTransactions(BaseModel):
    __tablename__ = 'transactions'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_ip = Column(VARCHAR(255), nullable=False)
    datetime = Column(DateTime, nullable=False)
    type = Column(VARCHAR(255), nullable=False)
    category_id = Column(Integer)
    goods_id = Column(Integer)
    cart_id = Column(Integer)
