from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.create_user import RequestCreateUserDto
from api.response.user import ResponseUserDto
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicPasswordHashException, SanicDBException, SanicUserConflictException

from db.queries import backend_users as backend_user_queries
from db.exceptions import DBDataException, DBIntegrityException, DBUserExistsException

from helpers.password import generate_hash
from helpers.password import GeneratePasswordHashException


class CreateUserEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateUserDto(body)

        try:
            hashed_password = generate_hash(request_model.password)
        except GeneratePasswordHashException as e:
            raise SanicPasswordHashException(str(e))

        try:
            db_user = backend_user_queries.create_backend_user(session, request_model, hashed_password)
        except DBUserExistsException:
            raise SanicUserConflictException('Login is busy')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseUserDto(db_user)

        return await self.make_response_json(body=response_model.dump(), status=201)
