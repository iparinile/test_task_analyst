from sqlalchemy import Column, Integer, VARCHAR

from db.models import BaseModel


class DBCategories(BaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)
