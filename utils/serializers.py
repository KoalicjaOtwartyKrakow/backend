import json
from uuid import UUID

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

from utils.orm import AccommodationUnit, Host, Guest


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(SQLAlchemyAutoSchema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


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


class HostSchema(CamelCaseSchema):
    class Meta:
        model = Host
        include_relationships = True
        include_fk = True
        load_instance = True


class GuestSchema(CamelCaseSchema):
    class Meta:
        model = Guest
        include_fk = True
        load_instance = True


class GuestSchemaFull(CamelCaseSchema):
    class Meta:
        model = Guest
        include_relationships = True
        include_fk = True
        load_instance = True

    accommodation_unit = fields.Nested(AccommodationUnitSchema)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)