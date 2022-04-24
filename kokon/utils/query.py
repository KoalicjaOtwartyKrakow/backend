import datetime
from typing import Type, Union, List, Set

from marshmallow import EXCLUDE, ValidationError
from marshmallow_sqlalchemy.schema import SQLAlchemySchema
from sqlalchemy import desc

from ..orm.base import Base
from ..serializers import camelcase, PaginationParamsSchema
from .functions import Request


def sort_stmt(
    stmt, request: Request, model: Base, exclude_columns: Union[List, Set, None] = None
):
    exclude_columns = exclude_columns or set()
    sort_column_cc = request.args.get("sort")
    if sort_column_cc:
        reverse = False
        if sort_column_cc and sort_column_cc[0] == "-":
            reverse = True
            sort_column_cc = sort_column_cc[1:]

        sort_columns_cc = {
            camelcase(c.name): c.name
            for c in model.__table__.columns
            if c.name not in exclude_columns
        }
        if sort_column_cc not in sort_columns_cc:
            raise ValidationError(
                f"Available sort options: {list(sort_columns_cc.keys())}.",
                field_name="sort",
            )
        sort_column = sort_columns_cc[sort_column_cc]

        if reverse:
            stmt = stmt.order_by(desc(getattr(model, sort_column)))
        else:
            stmt = stmt.order_by(getattr(model, sort_column))

    return stmt


def filter_stmt(
    stmt, request: Request, model: Base, exclude_columns: Union[List, Set, None] = None
):
    for column, column_type in [(c.name, c.type) for c in model.__table__.columns]:
        column_type_name = type(column_type).__name__

        if exclude_columns and column in exclude_columns:
            continue

        if column_type_name not in {
            "Enum",
            "Text",
            "String",
            "Integer",
            "TIMESTAMP",
            "Boolean",
        }:
            continue

        column_cc = camelcase(column)
        column_val = request.args.get(column_cc)

        cmp = "__eq__"
        if column_type_name in ("String", "Text"):
            if column_val and column_val.startswith("~"):
                cmp = "ilike"
                column_val = column_val[1:]
        elif column_type_name in {"Integer", "TIMESTAMP"}:
            for c in ("Gt", "Lt", "Gteq", "Lteq"):
                if column_cc + c in request.args:
                    column_val = request.args.get(column_cc + c)
                    cmp = f"__{c.lower()}__"
                    break

        if not column_val:
            continue

        if column_type_name == "Enum":
            if column_val not in column_type.enums:
                raise ValidationError(
                    f"Must be one of {column_type.enums}.", column=column_cc
                )

        if column_type_name == "TIMESTAMP":
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M"):
                try:
                    column_val = datetime.datetime.strptime(column_val, fmt)
                    break
                except ValueError:
                    pass
            else:
                raise ValidationError(f"DateTime format is invalid.", column=column_cc)

        if column_type_name == "Integer":
            try:
                column_val = int(column_val)
            except ValueError:
                raise ValidationError(f"Invalid number format.", column=column_cc)

        if column_type_name == "Boolean":
            column_val = True if column_val.lower() in {"t", "true", "1"} else False

        if cmp == "ilike":
            stmt = stmt.filter(getattr(model, column).ilike(f"%{column_val}%"))
        else:
            stmt = stmt.filter(getattr(getattr(model, column), cmp)(column_val))

    return stmt


def paginate(stmt, request: Request, schema: Type[SQLAlchemySchema]):
    # TODO(nanvel): for backward compatibility, remove later
    if "offset" not in request.args and "limit" not in request.args:
        return schema().dump(stmt.all(), many=True)

    params = PaginationParamsSchema().load(request.args, unknown=EXCLUDE)

    total = stmt.count()

    items = stmt.offset(params["offset"]).limit(params["limit"])

    return {"items": schema().dump(items, many=True), "total": total}
