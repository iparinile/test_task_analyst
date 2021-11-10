from api.base import ResponseDto
from api.exceptions import ValidationError


class ResponseAuthUserDtoSchema:

    def __init__(self, *args, **kwargs):
        self.fields = {'Authorization': ''}

    def load(self, data: dict) -> dict:

        valid_data = {}

        for key, value in data.items():
            if key not in self.fields:
                continue
            if not isinstance(value, self.fields[key].__class__):
                raise ValidationError(f'{key} should be str')

            valid_data[key] = value

        return valid_data


class ResponseAuthUserDto(ResponseDto):
    __schema__ = ResponseAuthUserDtoSchema


class AuthResponseObject:
    def __init__(self, token):
        self.Authorization = token
