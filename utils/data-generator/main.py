import click
from datasets import get_datasets
from generators import seed_generators, generate_host, generate_teammember, generate_languages, generate_accomodation_unit, generate_guest
from pyrnalist import report
from dotenv import load_dotenv


def to_pgsql_value(v):
    if isinstance(v, list):
        return "'{" + ", ".join([to_pgsql_value(x) for x in v]) + "}'"
    elif isinstance(v, str):
        return f"'{v}'"
    elif isinstance(v, bool):
        return 'true' if v else 'false'
    else:
        return str(v)


def to_sql(table, values):
    if len(values)>0:
        keys = values[0].keys()
        keys_quoted = [f'"{x}"' for x in keys]
        keys_str = ", ".join(keys_quoted)
        sql = f'INSERT INTO {table}({keys_str}) VALUES'
        value_inserts = []
        for v in values:
            values_str = ", ".join([to_pgsql_value(x) for x in v.values()])
            value_inserts.append(f'({values_str})')
        sql += ", ".join(value_inserts)
        print(sql)


@click.command()
@click.option('--count', default=1, help='Number of.')
@click.option('--teryt-path', help='Path to TERYT')
@click.option('--sql/', is_flag=True)
@click.option('--guests', is_flag=True)
@click.option('--hosts', is_flag=True)
@click.option('--accomodations', is_flag=True)
@click.option('--teammember', is_flag=True)
@click.option('--languages', is_flag=True)
@click.option('--db', is_flag=True)
def generate(count, teryt_path, sql, guests, hosts, accomodations, teammember, languages, db):
    datasets = get_datasets(teryt_path)
    seed_generators(datasets)
    all_guests = [generate_guest() for x in range(0, count)] if guests else []
    all_hosts = [generate_host() for x in range(0, count)] if hosts else []
    all_accomodations = [generate_accomodation_unit() for x in range(0, count)] if accomodations else []
    all_teammembers = [generate_teammember() for x in range(0, count)] if teammember else []

    if sql:
        to_sql('public.guests', all_guests) if guests else None
        to_sql('public.hosts', all_hosts) if hosts else None
        to_sql('public.accommodation_units', all_accomodations) if accomodations else None
        to_sql('public.teammembers', all_teammembers) if teammember else None

    if db:
        import psycopg2
        import os
        host = os.getenv('PSQL_HOST')
        database = os.getenv('PSQL_DATABASE')
        user = os.getenv('PSQL_USERNAME')
        password = os.getenv('PSQL_PASSWORD')
        port = os.getenv('PSQL_PORT')

        c = psycopg2.connect(f'dbname={database} user={user} password={password} host={host} port={port}')


if __name__ == '__main__':
    load_dotenv()
    generate()
    report.footer()
