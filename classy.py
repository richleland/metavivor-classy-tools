import csv
import json
from datetime import datetime
from pathlib import Path

import click

from api import (
    create_dedication,
    create_offline_transaction,
    get_campaigns_from_api,
    get_fundraising_pages_from_api,
    get_fundraising_teams_from_api,
)
from config import ORG_ID
from prepare import format_data


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
@click.argument("file_path", type=click.STRING)
def upload_transactions(campaign_id, file_path):
    path = Path(file_path)
    if not path.is_file():
        click.secho(f"{file_path} is not a valid file. Please retry with the path to a valid file.", fg="red")
        exit(1)

    # prepare the transaction data
    formatted = None
    with path.open() as csv_file:
        csv_data = csv.DictReader(csv_file)
        formatted = format_data(csv_data)

    if not formatted:
        click.secho("No formatted data to upload. Please check input CSV file.", fg="red")
        exit(1)

    click.echo(f"Transactions to process: {len(formatted)}")

    results = {}
    for item in formatted:
        transaction_payload = item["transaction"]
        dedication_payload = item["dedication"]

        transaction_result = create_offline_transaction(campaign_id, transaction_payload)
        transaction_id = transaction_result["id"]

        dedication_result = None
        if dedication_payload:
            dedication_result = create_dedication(transaction_id, dedication_payload)

        # store the API results
        results[transaction_id] = {
            "transaction": transaction_result,
            "dedication": dedication_result,
        }

    right_now = datetime.now().strftime("%Y-%m-%d-%H:%M")
    log_file_path = f"output/upload-results-{right_now}.csv"

    with open(log_file_path, "w") as f:
        json.dump(results, f, indent=2)

    click.secho(f"Done. Upload results logged to {log_file_path}")


cli.add_command(list_campaigns)
cli.add_command(list_teams)
cli.add_command(list_pages)
cli.add_command(upload_transactions)


if __name__ == "__main__":
    cli()
