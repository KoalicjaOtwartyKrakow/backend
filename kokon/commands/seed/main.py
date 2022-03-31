import itertools
from math import floor

import click
from pyrnalist import report

from kokon.utils.db import DB
from .datasets import get_datasets
from .generators import (
    seed_generators,
    generate_host,
    generate_teammember,
    generate_languages,
    generate_accommodation_unit,
    generate_guest,
)


def to_pgsql_value(v):
    if isinstance(v, list):
        return "'{" + ", ".join([to_pgsql_value(x) for x in v]) + "}'"
    elif isinstance(v, str):
        return f"$SomeTag${v}$SomeTag$"
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
    from .generators import  seed_generators
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
            session.execute(hosts_sql)
            session.execute(host_languages_sql)
            session.execute(accommodations_sql)
            session.execute(guests_sql)
            session.execute(teammembers_sql)

    if sql:
        print(hosts_sql)
        print(host_languages_sql)
        print(accommodations_sql)
        print(guests_sql)
        print(teammembers_sql)

    report.footer()


@click.command(name="load")
@click.option("--count", default=1, help="Number of.")
@click.option("--teryt-path", help="Path to TERYT")
@click.option("--sql/", is_flag=True, default=False)
@click.option("--db", is_flag=True, default=False)
@click.option("--sanitize", is_flag=True, default=False)
@click.option("--save", is_flag=True, default=False)
def load_cmd(count, teryt_path, sql, db, sanitize, save):
    from .importers.r3spreadsheet import (import_ludzi, import_recepcja, import_mieszkania, merge_ludzi_recepcja)
    ludzi = import_ludzi()
    recepcja = import_recepcja()

    report.info(f'Imported {len(ludzi)} from Ludzi')
    report.info(f'Imported {len(recepcja)} from UPD Data from Reception')

    merged = merge_ludzi_recepcja(ludzi, recepcja)
    report.info(f'Total guests after merge: {len(merged)}')

    (hosts, units, languages) = import_mieszkania(merged)
    report.info(f'Imported {len(hosts)} hosts from Mieszkania (live)')
    report.info(f'Imported {len(units)} units from Mieszkania (live)')
    report.info(f'Imported {len(languages)} languages from Mieszkania (live)')

    if sanitize:
        report.verbose('Sanitizing dataset')
        from .generators import (
            generate_host,
            generate_accommodation_unit,
            generate_guest,
        )

        load_dataset(teryt_path)

        for g in merged:
            sg = generate_guest(units)
            g['full_name'] = sg['full_name']
            g['phone_number'] = sg['phone_number']
            g['document_number'] = sg['document_number']

        for h in hosts:
            sh = generate_host()
            h['full_name'] = sh['full_name']
            h['email'] = sh['email']
            h['phone_number'] =  sh['phone_number']

        for au in units:
            sau = generate_accommodation_unit(hosts)
            au['zip'] = sau['zip']
            au['address_line'] = sau['address_line']

    hosts_sql = to_sql('public.hosts', hosts)
    host_languages_sql = to_sql('public.host_languages', languages)
    accommodations_sql = to_sql('public.accommodation_units', units)
    guests_sql = to_sql('public.guests', merged)

    if db:
        with DB().acquire() as session:
            session.execute(hosts_sql)
            session.execute(host_languages_sql)
            session.execute(accommodations_sql)
            session.execute(guests_sql)

    if sql:
        if save:
            with open("hosts.sql", 'w', encoding='utf-8') as f:
                f.write(hosts_sql)
            with open("host_languages.sql", 'w', encoding='utf-8') as f:
                f.write(host_languages_sql)
            with open("accommodations.sql", 'w', encoding='utf-8') as f:
                f.write(accommodations_sql)
            with open("guests.sql", 'w', encoding='utf-8') as f:
                f.write(guests_sql)
        else:
            print(hosts_sql)
            print(host_languages_sql)
            print(accommodations_sql)
            print(guests_sql)

    report.footer()
