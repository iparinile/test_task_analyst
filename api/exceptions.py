from sanic.exceptions import SanicException


class ApiValidationException(SanicException):
    status_code = 400


class ApiResponseValidationException(SanicException):
    status_code = 500


class ValidationError(SanicException):
    status_code = 400
