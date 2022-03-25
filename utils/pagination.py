
"""
Pagination functionality for endpoints returning large datasets.
Page info taken from request get params


Original code taken from
https://github.com/pallets/flask-sqlalchemy/blob/818c947b665206fe8edd8c1680b18ce83d3e4744/src/flask_sqlalchemy/__init__.py
And adjusted to needs of the project.
"""
from math import ceil

from marshmallow import EXCLUDE
from sqlalchemy import select
from sqlalchemy.sql.functions import count

DEFAULT_PER_PAGE = 20

DEFAULT_PAGE = 1

DEFAULT_MAX_PER_PAGE = 100
NO_MAX_PER_PAGE = object()


def get_pagination_from_request(request):
    """Get pagination information from request object"""
    from utils.serializers import PaginationSchema
    schema = PaginationSchema()
    params = schema.load(request.args, unknown=EXCLUDE)
    page = params.get('page', DEFAULT_PAGE)
    per_page = params.get('per_page', DEFAULT_PER_PAGE)
    return page, per_page


def get_statement_pagination(request, session, statement):
    """Get pagination object for sqlalchemy statement"""
    page, per_page = get_pagination_from_request(request)
    paginator = SqlAlchemyPaginator(session, statement)
    pagination = paginator.paginate(page, per_page)
    return pagination


class Paginator:
    """Paginator abstraction used to filter """
    def get_total(self):
        raise NotImplementedError(f"{self.__name__}.get_total must be implemented")

    def get_items(self, offset, limit):
        raise NotImplementedError(f"{self.__name__}.get_items must be implemented")

    def paginate(self, page=None, per_page=None, error_out=True, max_per_page=None, count=True):
        if page is None:
            page = DEFAULT_PAGE

        if per_page is None:
            per_page = DEFAULT_PER_PAGE

        if max_per_page is None:
            per_page = min(per_page, DEFAULT_MAX_PER_PAGE)
        elif max_per_page is not NO_MAX_PER_PAGE:
            per_page = min(per_page, max_per_page)

        if page < 1:
            if error_out:
                self.handle_pagination_error()
            else:
                page = DEFAULT_PAGE

        if per_page < 0:
            if error_out:
                self.handle_pagination_error()
            else:
                per_page = DEFAULT_PER_PAGE

        items = self.get_items((page - 1) * per_page, per_page)

        if not items and page != DEFAULT_PAGE and error_out:
            self.handle_pagination_error()

        total = None
        if count:
            total = self.get_total()

        return Pagination(self, page, per_page, total, items)

    def handle_pagination_error(self):
        pass


class SqlAlchemyPaginator(Paginator):
    """SQLAlchemy implementation for Paginator abstraction"""

    def __init__(self, session, statement):
        super(SqlAlchemyPaginator, self).__init__()
        self.session = session
        self.statement = statement

    def get_total(self):
        count_statement = select(count()).select_from(self.statement)
        total = self.session.execute(count_statement).scalar()
        return total

    def get_items(self, offset, limit):
        fetch_statement = self.statement.limit(limit).offset(offset)
        result = self.session.execute(fetch_statement)
        return result.scalars()


class Pagination:
    """Internal helper class returned by :meth:`BaseQuery.paginate`.  You
    can also construct it from any other SQLAlchemy query object if you are
    working with other libraries.  Additionally it is possible to pass `None`
    as query object in which case the :meth:`prev` and :meth:`next` will
    no longer work.
    """

    def __init__(self, paginator, page, per_page, total, items):
        #: the unlimited query object that was used to create this
        #: pagination object.
        self.paginator = paginator
        #: the current page number (1 indexed)
        self.page = page
        #: the number of items to be displayed on a page.
        self.per_page = per_page
        #: the total number of items matching the query
        self.total = total
        #: the items for the current page
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        if self.per_page == 0 or self.total is None:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self, error_out=False):
        """Returns a :class:`Pagination` object for the previous page."""
        assert (
                self.paginator is not None
        ), "a query object is required for this method to work"
        return self.paginator.paginate(self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        """Number of the previous page."""
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    def next(self, error_out=False):
        """Returns a :class:`Pagination` object for the next page."""
        assert (
                self.paginator is not None
        ), "a query object is required for this method to work"
        return self.paginator.paginate(self.page + 1, self.per_page, error_out)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        if not self.has_next:
            return None
        return self.page + 1

    def make_response(self, serializer_schema):
        extra = dict()
        if self.total is not None:
            extra['total'] = self.total
        results = [serializer_schema.dump(item) for item in self.items]
        return dict(
            page=self.page,
            per_page=self.per_page,
            results=results,
            **extra)

