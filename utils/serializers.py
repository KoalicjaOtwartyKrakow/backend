import json
from uuid import UUID

from marshmallow import Schema
from marshmallow.fields import Integer
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields, auto_field

from utils.orm import AccommodationUnit, Host, Guest, Language, User


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(SQLAlchemyAutoSchema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    camel_case = True

    def __init__(self, camel_case=True, *args, **kwargs):
        self.camel_case = camel_case
        super().__init__(*args, **kwargs)

    def on_bind_field(self, field_name, field_obj):
        if not self.camel_case:
            return

        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class PaginationSchema(Schema):
    """
    Schema that does validation for pagination inputs in the request object

    Used in: utils.pagination.get_pagination_from_request
    """

    page = Integer(allow_none=True)
    per_page = Integer(data_key='per-page', allow_none=True)


class LanguageSchema(CamelCaseSchema):
    class Meta:
        model = Language
        include_fk = True
        load_instance = True


class HostSchema(CamelCaseSchema):
    class Meta:
        model = Host
        include_fk = True
        load_instance = True

    languages_spoken = fields.Nested("LanguageSchema", many=True)


class GuestSchema(CamelCaseSchema):
    class Meta:
        model = Guest
        include_fk = True
        load_instance = True

    claimed_at = auto_field(dump_only=True)


class GuestSchemaFull(CamelCaseSchema):
    class Meta:
        model = Guest
        include_relationships = True
        include_fk = True
        load_instance = True

    accommodation_unit = fields.Nested("AccommodationUnitSchema")


class AccommodationUnitSchema(CamelCaseSchema):
    class Meta:
        model = AccommodationUnit
        include_fk = True
        load_instance = True


class AccommodationUnitSchemaFull(CamelCaseSchema):
    class Meta:
        model = AccommodationUnit
        include_relationships = True
        include_fk = True
        load_instance = True

    host = fields.Nested("HostSchema")
    guests = fields.Nested("GuestSchema", many=True)


class UserSchema(CamelCaseSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)
