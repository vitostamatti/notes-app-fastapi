import click
from app.database.db_init import init, reset

@click.group()
def cli():
    pass

@click.command()
def db_init():
    init()
    click.echo('Initialized the database and created tables')

@click.command()
def db_reset():
    reset()
    click.echo('Dropped all tables in the the database')

cli.add_command(db_init)
cli.add_command(db_reset)

if __name__ == '__main__':
    cli()