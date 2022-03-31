import click

from .load import load_cmd
from .seed import seed_cmd


@click.group()
def cli():
    pass


cli.add_command(load_cmd)
cli.add_command(seed_cmd)
