import click
from pyrnalist import report

from kokon.utils.db import DB
from ..seed.generators import generate_accommodation_unit, generate_guest, generate_host
from ..seed.main import load_dataset, to_sql
from .r3spreadsheet import (
    import_ludzi,
    merge_ludzi_recepcja,
    import_mieszkania,
    import_recepcja,
)


@click.command(name="load")
@click.option("--teryt-path", help="Path to TERYT")
@click.option("--sql/", is_flag=True, default=False)
@click.option("--db", is_flag=True, default=False)
@click.option("--sanitize", is_flag=True, default=False)
@click.option("--save", is_flag=True, default=False)
def load_cmd(teryt_path, sql, db, sanitize, save):
    ludzi = import_ludzi()
    recepcja = import_recepcja()

    report.info(f"Imported {len(ludzi)} from Ludzi")
    report.info(f"Imported {len(recepcja)} from UPD Data from Reception")

    merged = merge_ludzi_recepcja(ludzi, recepcja)
    report.info(f"Total guests after merge: {len(merged)}")

    (hosts, units, languages) = import_mieszkania(merged)
    report.info(f"Imported {len(hosts)} hosts from Mieszkania (live)")
    report.info(f"Imported {len(units)} units from Mieszkania (live)")
    report.info(f"Imported {len(languages)} languages from Mieszkania (live)")

    if sanitize:
        report.verbose("Sanitizing dataset")

        load_dataset(teryt_path)

        for g in merged:
            sg = generate_guest(units)
            g["full_name"] = sg["full_name"]
            g["phone_number"] = sg["phone_number"]
            g["document_number"] = sg["document_number"]

        for h in hosts:
            sh = generate_host()
            h["full_name"] = sh["full_name"]
            h["email"] = sh["email"]
            h["phone_number"] = sh["phone_number"]

        for au in units:
            sau = generate_accommodation_unit(hosts)
            au["zip"] = sau["zip"]
            au["address_line"] = sau["address_line"]

    hosts_sql = to_sql("public.hosts", hosts)
    host_languages_sql = to_sql("public.host_languages", languages)
    accommodations_sql = to_sql("public.accommodation_units", units)
    guests_sql = to_sql("public.guests", merged)

    if db:
        with DB().acquire() as session:
            session.execute(hosts_sql)
            session.execute(host_languages_sql)
            session.execute(accommodations_sql)
            session.execute(guests_sql)

    if sql:
        if save:
            with open("hosts.sql", "w", encoding="utf-8") as f:
                f.write(hosts_sql)
            with open("host_languages.sql", "w", encoding="utf-8") as f:
                f.write(host_languages_sql)
            with open("accommodations.sql", "w", encoding="utf-8") as f:
                f.write(accommodations_sql)
            with open("guests.sql", "w", encoding="utf-8") as f:
                f.write(guests_sql)
        else:
            print(hosts_sql)
            print(host_languages_sql)
            print(accommodations_sql)
            print(guests_sql)

    report.footer()
