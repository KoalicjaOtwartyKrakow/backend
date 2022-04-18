"""triggers

Revision ID: 1668bb143660
Revises: 18145559121e
Create Date: 2022-04-14 22:40:19.042558

"""
from alembic import op

from kokon.utils.auditing import sync_trigger, drop_trigger


# revision identifiers, used by Alembic.
revision = "1668bb143660"
down_revision = "18145559121e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()

    # Enable hstore extension (used by versioning triggers)
    op.execute("CREATE EXTENSION IF NOT EXISTS hstore WITH SCHEMA public")

    op.execute(
        """
    CREATE OR REPLACE FUNCTION transaction_temp_table_generator()
    RETURNS TRIGGER AS $$
    BEGIN
        CREATE TEMP TABLE IF NOT EXISTS
            temporary_transaction (id BIGINT, PRIMARY KEY(id))
        ON COMMIT DELETE ROWS;
        INSERT INTO temporary_transaction (id) VALUES (NEW.id);
        RETURN NEW;
    END;
    $$
    LANGUAGE plpgsql
    """
    )

    op.execute(
        """
    CREATE TRIGGER transaction_trigger
    AFTER INSERT ON transaction
    FOR EACH ROW EXECUTE PROCEDURE transaction_temp_table_generator()
    """
    )

    sync_trigger(conn, "guests_version")
    sync_trigger(conn, "accommodation_units_version")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    drop_trigger(conn, "guests")
    drop_trigger(conn, "accommodation_units")

    op.execute("DROP TRIGGER transaction_trigger ON transaction;")
    op.execute("DROP FUNCTION transaction_temp_table_generator();")
    # ### end Alembic commands ###
