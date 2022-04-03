from typing import Type

from marshmallow import EXCLUDE
from marshmallow_sqlalchemy.schema import SQLAlchemySchema

from ..serializers import PaginationParamsSchema
from .functions import Request


def paginate(stmt, request: Request, schema: Type[SQLAlchemySchema]):
    params = PaginationParamsSchema().load(request.args, unknown=EXCLUDE)

    total = stmt.count()
    items = stmt.offset(params["offset"]).limit(params["limit"])

    return {"items": schema().dump(items, many=True), "total": total}
