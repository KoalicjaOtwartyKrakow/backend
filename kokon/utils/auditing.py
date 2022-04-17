import sqlalchemy as sa
from sqlalchemy_continuum.dialects.postgresql import create_trigger, drop_trigger


def sync_trigger(conn, table_name):
    """
    A copy of sqlalchemy_continuum.dialects.postgresql.sync_trigger.
    Added use_property_mod_tracking=False
    because version model does not have mod fields.
    """
    meta = sa.MetaData()
    version_table = sa.Table(table_name, meta, autoload=True, autoload_with=conn)
    parent_table = sa.Table(
        table_name[0 : -len("_version")], meta, autoload=True, autoload_with=conn
    )
    excluded_columns = set(c.name for c in parent_table.c) - set(
        c.name for c in version_table.c if not c.name.endswith("_mod")
    )
    drop_trigger(conn, parent_table.name)
    create_trigger(
        conn,
        table=parent_table,
        excluded_columns=excluded_columns,
        use_property_mod_tracking=False,
    )
