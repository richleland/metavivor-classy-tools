import click

from api import get_campaigns_from_api, get_fundraising_pages_from_api, get_fundraising_teams_from_api
from config import ORG_ID


@click.group()
def cli():
    pass


@click.command()
def list_campaigns():
    campaigns = get_campaigns_from_api(ORG_ID)
    click.echo(f"Number of campaigns: {len(campaigns)}")
    if campaigns:
        click.echo("The following campaigns are in Classy:")
    for campaign in campaigns:
        click.echo(f"[{campaign['id']}] {campaign['name']}")


@click.command()
@click.argument("campaign_id", type=click.INT)
def list_teams(campaign_id):
    teams = get_fundraising_teams_from_api(campaign_id)
    click.echo(f"Number of teams: {len(teams)}")
    if teams:
        click.echo("The following teams are in Classy:")
        for team in teams:
            click.echo(f"[{team['id']}] {team['name']}")


@click.command()
@click.argument("campaign_id", type=click.INT)
def list_pages(campaign_id):
    pages = get_fundraising_pages_from_api(campaign_id)
    click.echo(f"Number of pages: {len(pages)}")
    if pages:
        click.echo("The following pages are in Classy:")
        for page in pages:
            click.echo(f"[{page['id']}] {page['alias']}")


cli.add_command(list_campaigns)
cli.add_command(list_teams)
cli.add_command(list_pages)


if __name__ == "__main__":
    cli()
