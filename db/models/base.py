from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def __repr__(self):
        return f'{self.__class__.__name__}'
