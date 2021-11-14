from sqlalchemy import Column, VARCHAR, Integer, ForeignKey

from db.models import BaseModel


class DBGoods(BaseModel):
    __tablename__ = 'goods'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    name = Column(VARCHAR(255), nullable=False, unique=False)
