from sqlalchemy import Column, VARCHAR, Integer

from db.models import BaseModel


class DBGoods(BaseModel):
    __tablename__ = 'goods'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)
    category_id = Column(Integer, nullable=False)
