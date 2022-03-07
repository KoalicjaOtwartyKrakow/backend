import click
from datasets import get_datasets
from generators import seed_generators, generate_host


@click.command()
@click.option('--count', default=1, help='Number of.')
def generate(count):
    datasets = get_datasets()
    seed_generators(datasets)
    for x in range(0, 10):
        generate_host()


if __name__ == '__main__':
    generate()
