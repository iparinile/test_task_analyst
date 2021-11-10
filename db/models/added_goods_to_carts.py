from sqlalchemy import Column, Integer

from db.models import BaseModel


class DBAddedGoodsToCarts(BaseModel):
    __tablename__ = 'added_goods_to_carts'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    # А может просто Carts?
