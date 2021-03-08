import json
from datetime import datetime

import click

from api import (
    create_offline_transactions,
    get_campaigns_from_api,
    get_fundraising_pages_from_api,
    get_fundraising_teams_from_api,
)
from config import ORG_ID


@click.group()
def cli():
    pass


@click.command()
def list_campaigns():
    campaigns = get_campaigns_from_api(ORG_ID)
    click.echo(f"Number of campaigns: {len(campaigns)}")
    if campaigns:
        click.secho("The following campaigns are in Classy:", fg="green")
    for campaign in campaigns:
        click.echo(f"[{campaign['id']}] {campaign['name']}")


@click.command()
@click.argument("campaign_id", type=click.INT)
def list_teams(campaign_id):
    teams = get_fundraising_teams_from_api(campaign_id)
    click.echo(f"Number of teams: {len(teams)}")
    if teams:
        click.secho("The following teams are in Classy:", fg="green")
        for team in teams:
            click.echo(f"[{team['id']}] {team['name']}")


@click.command()
@click.argument("campaign_id", type=click.INT)
def list_pages(campaign_id):
    pages = get_fundraising_pages_from_api(campaign_id)
    click.echo(f"Number of pages: {len(pages)}")
    if pages:
        click.secho("The following pages are in Classy:", fg="green")
        for page in pages:
            click.echo(f"[{page['id']}] {page['alias']}")


@click.command()
@click.argument("campaign_id", type=click.INT)
def upload_transactions(campaign_id):
    """
    TODO: make this handle multiple inputs, not just a single record.
    Logs for example should include multiple records
    """
    with open("input/test-transaction.json") as f:
        payload = json.load(f)

    result = create_offline_transactions(campaign_id, payload)
    right_now = datetime.now().strftime("%Y-%m-%d-%H:%M")
    file_path = f"output/upload-results-{right_now}.csv"

    with open(file_path, "w") as f:
        json.dump(result, f, indent=2)

    click.secho(f"Done. Upload results logged to {file_path}")


cli.add_command(list_campaigns)
cli.add_command(list_teams)
cli.add_command(list_pages)
cli.add_command(upload_transactions)


if __name__ == "__main__":
    cli()
