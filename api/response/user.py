import datetime

from marshmallow import Schema, fields, pre_load, post_load

from api.base import ResponseDto


class ResponseUserDtoSchema(Schema):
    id = fields.Int(required=True)
    login = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    update_at = fields.DateTime(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    @pre_load
    @post_load
    def deserialize_datetime(self, data: dict, **kwargs) -> dict:
        if 'created_at' in data:
            data['created_at'] = self.datetime_to_iso(data['created_at'])
        if 'update_at' in data:
            data['update_at'] = self.datetime_to_iso(data['update_at'])

        return data

    @staticmethod
    def datetime_to_iso(dt):
        if isinstance(dt, datetime.datetime):
            return dt.isoformat()
        return dt


class ResponseUserDto(ResponseDto, ResponseUserDtoSchema):
    __schema__ = ResponseUserDtoSchema
