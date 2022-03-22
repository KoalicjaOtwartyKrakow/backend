class BaseRepo:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def row_to_dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        return d
