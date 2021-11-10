import datetime

from sqlalchemy import Column, VARCHAR, VARBINARY, BOOLEAN, TIMESTAMP, Integer

from db.models import BaseModel


class DBBackendUsers(BaseModel):
    __tablename__ = 'backend_users'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    update_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_delete = Column(BOOLEAN(), nullable=False, default=False)
    login = Column(VARCHAR(255), nullable=False, unique=True)
    password = Column(VARBINARY(), nullable=False)
    first_name = Column(VARCHAR(255))
    last_name = Column(VARCHAR(255))
