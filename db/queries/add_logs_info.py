from db.database import DBSession
from db.models import DBUsers


def create_user(session: DBSession, user_ip: str, user_id: int, country: str = '') -> None:

    new_user = DBUsers(
        ip=user_ip,
        id=user_id,
        country=country
    )

    session.add_model(new_user)
