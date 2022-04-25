"""app_role

Revision ID: 3d11101cebad
Revises: 18145559121e
Create Date: 2022-04-20 21:11:14.192326

"""
import os

from alembic import op


# revision identifiers, used by Alembic.
revision = "3d11101cebad"
down_revision = "18145559121e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    # don't create the role for test db
    if "test" in conn.engine.url.database:
        user_name = "test_user"
        user_password = "postgres"
    else:
        user_name = os.getenv("db_app_user", None)
        user_password = os.getenv("db_app_pass", None)

    if not (user_name and user_password):
        raise AssertionError("db_app_user or db_app_pass env variables are missing.")

    op.execute(f"CREATE USER {user_name} WITH PASSWORD '{user_password}';")
    op.execute(
        f"""
        DO
        $$
        BEGIN
            execute format('GRANT CONNECT ON DATABASE %I TO {user_name}', current_database());
        END;
        $$;
        """
    )

    op.execute(
        f"""
        GRANT USAGE ON SCHEMA public TO {user_name};
        GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public to {user_name};
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {user_name};
        -- reduce permissions for _version tables
        REVOKE ALL ON accommodation_units_version FROM {user_name};
        GRANT INSERT, UPDATE(end_transaction_id), SELECT(guid, transaction_id) ON TABLE accommodation_units_version TO {user_name};
        REVOKE ALL ON guests_version FROM {user_name};
        GRANT INSERT, UPDATE(end_transaction_id), SELECT(guid, transaction_id) ON TABLE guests_version TO {user_name};
        GRANT EXECUTE ON FUNCTION update_claimed_at() TO {user_name};
        -- default roles assigned to new objects in future
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO {user_name};
        """
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    if "test" in conn.engine.url.database:
        user_name = "test_user"
    else:
        user_name = os.getenv("db_app_user", None)

    if not user_name:
        raise AssertionError("db_app_user variable is missing.")

    op.execute(
        f"""
        DO
        $$
        BEGIN
            IF EXISTS (SELECT FROM pg_roles WHERE rolname = '{user_name}') THEN
                DROP OWNED BY {user_name};
                DROP USER {user_name};
            END IF;
        END
        $$;
        """
    )
    # ### end Alembic commands ###
