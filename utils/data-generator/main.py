import itertools
from math import floor

import click
from datasets import get_datasets
from generators import (
    seed_generators,
    generate_host,
    generate_teammember,
    generate_languages,
    generate_accommodation_unit,
    generate_guest,
)
from pyrnalist import report
from dotenv import load_dotenv


def to_pgsql_value(v):
    if isinstance(v, list):
        return "'{" + ", ".join([to_pgsql_value(x) for x in v]) + "}'"
    elif isinstance(v, str):
        return f"'{v}'"
    elif isinstance(v, bool):
        return "true" if v else "false"
    elif v is None:
        return "null"
    else:
        return str(v)


def to_sql(table, values):
    if len(values) > 0:
        keys = values[0].keys()
        keys_quoted = [f'"{x}"' for x in keys]
        keys_str = ", ".join(keys_quoted)
        sql = f"INSERT INTO {table}({keys_str}) VALUES"
        value_inserts = []
        for v in values:
            values_str = ", ".join([to_pgsql_value(x) for x in v.values()])
            value_inserts.append(f"({values_str})")
        sql += ", ".join(value_inserts)
        print(sql + ";")


@click.command()
@click.option("--count", default=1, help="Number of.")
@click.option("--teryt-path", help="Path to TERYT")
@click.option("--sql/", is_flag=True)
@click.option("--db", is_flag=True)
def generate(count, teryt_path, sql, db):
    datasets = get_datasets(teryt_path)
    seed_generators(datasets)

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

    if sql:
        to_sql("public.hosts", all_hosts)
        print()
        to_sql("public.host_languages", all_host_languages)
        print()
        to_sql("public.accommodation_units", all_accomodations)
        print()
        to_sql("public.guests", all_guests)
        print()
        to_sql("public.teammembers", all_teammembers)


if __name__ == "__main__":
    load_dotenv()
    generate()
    report.footer()
