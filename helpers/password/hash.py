import bcrypt

from helpers.password.exception import GeneratePasswordHashException, CheckPasswordHashException


def generate_hash(pwd: str) -> bytes:
    try:
        return bcrypt.hashpw(
            password=pwd.encode(),
            salt=bcrypt.gensalt()
        )
    except (TypeError, ValueError) as e:
        raise GeneratePasswordHashException(str(e))


def check_hash(pwd: str, hsh: bytes) -> None:
    try:
        result = bcrypt.checkpw(
            password=pwd.encode(),
            hashed_password=hsh
        )
    except (TypeError, ValueError) as e:
        raise CheckPasswordHashException(str(e))

    if not result:
        raise CheckPasswordHashException
