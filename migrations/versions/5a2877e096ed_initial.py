"""initial

Revision ID: 5a2877e096ed
Revises: 
Create Date: 2022-03-20 21:22:58.439923

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5a2877e096ed"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    op.create_table(
        "hosts",
        sa.Column(
            "guid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("full_name", sa.String(length=256), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column("call_after", sa.String(length=64), nullable=True),
        sa.Column("call_before", sa.String(length=64), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("CREATED", "VERIFIED", "REJECTED", name="verificationstatus"),
            server_default="CREATED",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("system_comments", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("guid"),
    )
    op.create_table(
        "languages",
        sa.Column("name", sa.String(length=20), nullable=True),
        sa.Column("code2", sa.String(length=2), nullable=False),
        sa.Column("code3", sa.String(length=3), nullable=True),
        sa.PrimaryKeyConstraint("code2"),
    )
    op.create_table(
        "teammembers",
        sa.Column(
            "guid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("full_name", sa.String(length=100), nullable=True),
        sa.Column("phone_number", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("guid"),
    )
    op.create_table(
        "accommodation_units",
        sa.Column(
            "guid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("host_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("city", sa.String(length=50), nullable=True),
        sa.Column("zip", sa.String(length=10), nullable=False),
        sa.Column(
            "voivodeship",
            sa.Enum(
                "DOLNOSLASKIE",
                "KUJAWSKOPOMORSKIE",
                "LUBELSKIE",
                "LUBUSKIE",
                "LODZKIE",
                "MALOPOLSKIE",
                "MAZOWIECKIE",
                "OPOLSKIE",
                "PODKARPACKIE",
                "PODLASKIE",
                "POMORSKIE",
                "SLASKIE",
                "SWIETOKRZYSKIE",
                "WARMINSKOMAZURSKIE",
                "WIELKOPOLSKIE",
                "ZACHODNIOPOMORSKIE",
                name="voivodeship",
            ),
            nullable=True,
        ),
        sa.Column("address_line", sa.String(length=512), nullable=False),
        sa.Column("vacancies_total", sa.Integer(), nullable=False),
        sa.Column("pets_present", sa.Boolean(), nullable=True),
        sa.Column("pets_accepted", sa.Boolean(), nullable=True),
        sa.Column("disabled_people_friendly", sa.Boolean(), nullable=True),
        sa.Column("lgbt_friendly", sa.Boolean(), nullable=True),
        sa.Column("parking_place_available", sa.Boolean(), nullable=True),
        sa.Column("owner_comments", sa.Text(), nullable=True),
        sa.Column("easy_ambulance_access", sa.Boolean(), nullable=True),
        sa.Column("vacancies_free", sa.Integer(), nullable=True),
        sa.Column("staff_comments", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("CREATED", "VERIFIED", "REJECTED", name="verificationstatus"),
            server_default="CREATED",
            nullable=False,
        ),
        sa.Column("system_comments", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["host_id"], ["hosts.guid"], name="fk_host"),
        sa.PrimaryKeyConstraint("guid"),
    )
    op.create_table(
        "host_languages",
        sa.Column("language_code", sa.String(length=2), nullable=True),
        sa.Column("host_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "guid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["host_id"], ["hosts.guid"], name="fk_host"),
        sa.ForeignKeyConstraint(
            ["language_code"], ["languages.code2"], name="fk_language"
        ),
        sa.PrimaryKeyConstraint("guid"),
        sa.UniqueConstraint("language_code", "host_id", name="lang_host_pair_unique"),
    )
    op.create_table(
        "guests",
        sa.Column(
            "guid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column(
            "is_agent", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
        sa.Column("document_number", sa.String(length=255), nullable=True),
        sa.Column(
            "people_in_group", sa.Integer(), server_default=sa.text("1"), nullable=False
        ),
        sa.Column(
            "adult_male_count",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column(
            "adult_female_count",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column("children_ages", postgresql.ARRAY(sa.Integer()), nullable=False),
        sa.Column(
            "have_pets", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
        sa.Column("pets_description", sa.String(length=255), nullable=True),
        sa.Column("special_needs", sa.Text(), nullable=True),
        sa.Column("food_allergies", sa.Text(), nullable=True),
        sa.Column(
            "meat_free_diet",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "gluten_free_diet",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "lactose_free_diet",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("finance_status", sa.String(length=255), nullable=True),
        sa.Column("how_long_to_stay", sa.String(length=255), nullable=True),
        sa.Column("desired_destination", sa.String(length=255), nullable=True),
        sa.Column(
            "priority_status",
            sa.Enum(
                "DOES_NOT_RESPOND",
                "ACCOMMODATION_NOT_NEEDED",
                "EN_ROUTE_UA",
                "EN_ROUTE_PL",
                "IN_KRK",
                "AT_R3",
                "ACCOMMODATION_FOUND",
                "UPDATED",
                name="guestprioritystatus",
            ),
            nullable=True,
        ),
        sa.Column(
            "priority_date",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("staff_comments", sa.Text(), nullable=True),
        sa.Column(
            "verification_status",
            sa.Enum("CREATED", "VERIFIED", "REJECTED", name="verificationstatus"),
            server_default="CREATED",
            nullable=False,
        ),
        sa.Column("system_comments", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "accommodation_unit_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["accommodation_unit_id"],
            ["accommodation_units.guid"],
            name="fk_accommodation_unit_id",
        ),
        sa.PrimaryKeyConstraint("guid"),
    )

    op.execute(
        """
        INSERT INTO public.languages("name", code2, code3)
        VALUES
            ('English',	'en',	'eng'),
            ('Ukrainian',	'uk',	'ukr'),
            ('Polish',	'pl',	'pol'),
            ('Russian',	'ru',	'rus');
        """
    )

    op.execute(
        """
        DO
        $$
        BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_catalog.pg_user
                WHERE usename = 'apiserviceuser') THEN
                    CREATE USER ApiServiceUser WITH PASSWORD 'aB94cgg4s?FkLzsi';
                    ALTER DEFAULT PRIVILEGES IN SCHEMA public
                    GRANT select,insert,update,delete,truncate ON TABLES TO ApiServiceUser;
                    GRANT select,insert,update,delete,truncate ON ALL TABLES IN schema public TO ApiServiceUser;
                    REVOKE select,insert,update,delete,truncate ON public.languages from ApiServiceUser;
            END IF;
        END
        $$;
        """
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("guests")
    op.drop_table("host_languages")
    op.drop_table("accommodation_units")
    op.drop_table("teammembers")
    op.drop_table("languages")
    op.drop_table("hosts")

    op.execute("DROP TYPE verificationstatus;")
    op.execute("DROP TYPE voivodeship;")
    op.execute("DROP TYPE guestprioritystatus;")

    op.execute("DROP OWNED BY ApiServiceUser; DROP USER ApiServiceUser;")
    # ### end Alembic commands ###
