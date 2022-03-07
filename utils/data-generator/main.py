import click
from datasets import get_datasets
from generators import seed_generators, generate_host, generate_teammember, generate_languages, generate_accomodation_unit
from pyrnalist import report

@click.command()
@click.option('--count', default=1, help='Number of.')
@click.option('--teryt-path', help='Path to TERYT')
def generate(count, teryt_path):
    datasets = get_datasets(teryt_path)
    seed_generators(datasets)
    for x in range(0, 10):
        print(generate_accomodation_unit())


if __name__ == '__main__':
    generate()
    report.footer()
