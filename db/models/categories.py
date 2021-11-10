from sqlalchemy import Column, Integer, VARCHAR

from db.models import BaseModel


class DBCategories(BaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)
