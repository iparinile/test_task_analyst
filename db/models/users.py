from sqlalchemy import Column, VARCHAR, Integer

from db.models import BaseModel


class DBUsers(BaseModel):
    __tablename__ = 'users'

    ip = Column(VARCHAR(255), nullable=False, unique=True, primary_key=True)
    id = Column(Integer, unique=True)
    country = Column(VARCHAR(255))
