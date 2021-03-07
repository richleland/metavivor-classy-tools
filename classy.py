import click

from upload import get_teams_from_api


@click.group()
def cli():
    pass


@click.command()
def show_teams():
    teams = get_teams_from_api(319115)
    click.echo(f"Number of teams: {len(teams)}")
    click.echo("The following teams are in Classy:")
    for team in teams:
        click.echo(f"[{team['id']}] {team['name']}")


cli.add_command(show_teams)


if __name__ == "__main__":
    cli()
