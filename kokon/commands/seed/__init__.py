import itertools
from math import floor

import click
from pyrnalist import report
from sqlalchemy import text

from kokon.utils.db import DB
from .generators import (
    generate_host,
    generate_teammember,
    generate_languages,
    generate_accommodation_unit,
    generate_guest,
)


def to_pgsql_value(v):
    if isinstance(v, str):
        return f"$SomeTag${v}$SomeTag$"
    elif isinstance(v, list):
        return "'{" + ", ".join([to_pgsql_value(x) for x in v]) + "}'"
    elif isinstance(v, bool):
        return "true" if v else "false"
    elif v is None:
        return "null"
    else:
        return str(v)


def to_sql(table, values):
    if len(values) > 0:
        keys = [k for k in values[0].keys() if not k.startswith("__")]
        keys_quoted = [f'"{x}"' for x in keys]
        keys_str = ", ".join(keys_quoted)
        sql = f"INSERT INTO {table}({keys_str}) VALUES"
        value_inserts = []
        for v in values:
            values_str = ", ".join([to_pgsql_value(v[x]) for x in keys])
            value_inserts.append(f"({values_str})")
        sql += ", ".join(value_inserts)
        return sql + ";"


def load_dataset(teryt_path):
    from .datasets import get_datasets
    from .generators import seed_generators

    datasets = get_datasets(teryt_path)
    seed_generators(datasets)


@click.command(name="seed")
@click.option("--count", default=1, help="Number of.")
@click.option("--teryt-path", help="Path to TERYT")
@click.option("--sql/", is_flag=True, default=False)
@click.option("--db", is_flag=True, default=False)
def seed_cmd(count, teryt_path, sql, db):
    load_dataset(teryt_path)

    all_hosts = [generate_host() for _ in range(count)]
    # generate languages for 80% of hosts, 1-4 languages per host
    all_host_languages = list(
        itertools.chain.from_iterable(
            (generate_languages(host) for host in all_hosts[floor(count / 5) :])
        )
    )
    all_accomodations = [generate_accommodation_unit(all_hosts) for _ in range(count)]
    all_guests = [generate_guest(all_accomodations) for _ in range(count)]
    all_teammembers = [generate_teammember() for _ in range(count)]

    hosts_sql = to_sql("public.hosts", all_hosts)
    host_languages_sql = to_sql("public.host_languages", all_host_languages)
    accommodations_sql = to_sql("public.accommodation_units", all_accomodations)
    guests_sql = to_sql("public.guests", all_guests)
    teammembers_sql = to_sql("public.teammembers", all_teammembers)

    if db:
        with DB().acquire() as session:
            session.execute(text(hosts_sql))
            session.execute(text(host_languages_sql))
            session.execute(text(accommodations_sql))
            session.execute(text(guests_sql))
            session.execute(text(teammembers_sql))

    if sql:
        print(hosts_sql)
        print(host_languages_sql)
        print(accommodations_sql)
        print(guests_sql)
        print(teammembers_sql)

    report.footer()
