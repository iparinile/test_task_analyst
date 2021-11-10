from sqlalchemy import Column, Integer, Boolean

from db.models import BaseModel


class DBCarts(BaseModel):
    __tablename__ = 'carts'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    is_payed = Column(Boolean, default=False, nullable=False)
