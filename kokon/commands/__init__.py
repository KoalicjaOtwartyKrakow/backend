import click

from .seed.main import seed_cmd


@click.group()
def cli():
    pass


cli.add_command(seed_cmd)
