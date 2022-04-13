from typing import Type

from marshmallow import EXCLUDE
from marshmallow_sqlalchemy.schema import SQLAlchemySchema

from ..serializers import PaginationParamsSchema
from .functions import Request


def paginate(stmt, request: Request, schema: Type[SQLAlchemySchema]):
    # TODO(nanvel): for backward compatibility, remove later
    if "offset" not in request.args and "limit" not in request.args:
        return schema().dump(stmt.all(), many=True)

    params = PaginationParamsSchema().load(request.args, unknown=EXCLUDE)

    total = stmt.count()
    items = stmt.offset(params["offset"]).limit(params["limit"])

    return {"items": schema().dump(items, many=True), "total": total}
