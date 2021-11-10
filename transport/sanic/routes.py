from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return (
        endpoints.HealthEndpoint(config=config, context=context, uri='/', methods=['GET', 'POST']),
        endpoints.CreateUserEndpoint(config=config, context=context, uri='/user', methods=['POST']),
        endpoints.AuthUserEndpoint(config, context, uri='/user/auth', methods=['POST']),
        endpoints.UserEndpoint(config, context, uri='/user/<uid:int>', methods=['PATCH', 'DELETE'],
                               auth_required=True),
        endpoints.AllUserEndpoint(config, context, uri='/user/all', methods=['GET'], auth_required=True),
        endpoints.ParseLogsEndpoint(config, context, uri='/parse', methods=['GET'], auth_required=True)
    )
