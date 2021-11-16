from typing import List

from api.request import RequestCreateUserDto, RequestPatchUserDto
from db.database import DBSession
from db.exceptions import DBUserExistsException, DBUserNotExistsException
from db.models import DBBackendUsers


def create_backend_user(session: DBSession, user: RequestCreateUserDto, hashed_password: bytes) -> DBBackendUsers:
    new_user = DBBackendUsers(
        login=user.login,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )

    if session.get_backend_user_by_login(new_user.login) is not None:
        raise DBUserExistsException

    session.add_model(new_user)

    return new_user


def get_user(session: DBSession, *, login: str = None, user_id: int = None) -> DBBackendUsers:
    db_user = None

    if login is not None:
        db_user = session.get_backend_user_by_login(login)
    elif user_id is not None:
        db_user = session.get_backend_user_by_id(user_id)

    if db_user is None:
        raise DBUserNotExistsException
    return db_user


def patch_user(session: DBSession, user: RequestPatchUserDto, user_id: int) -> DBBackendUsers:
    db_user = session.get_backend_user_by_id(user_id)

    for attr in user.fields:
        if hasattr(user, attr):
            value = getattr(user, attr)
            setattr(db_user, attr, value)

    return db_user


def delete_user(session: DBSession, user_id: int) -> DBBackendUsers:
    db_user = session.get_backend_user_by_id(user_id)
    db_user.is_delete = True
    return db_user


def get_users(session: DBSession) -> List['DBBackendUsers']:
    return session.get_user_all()
