import click

from .seed.main import (seed_cmd, load_cmd)


@click.group()
def cli():
    pass


cli.add_command(seed_cmd)
cli.add_command(load_cmd)
