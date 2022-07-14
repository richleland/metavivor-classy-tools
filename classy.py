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
    """List the campaigns for your organization"""
    campaigns = get_campaigns_from_api(ORG_ID)
    click.echo(f"Number of campaigns: {len(campaigns)}")
    if campaigns:
        click.secho("The following campaigns are in Classy:", fg="green")
    for campaign in campaigns:
        click.echo(f"[{campaign['id']}] {campaign['name']}")


@click.command()
@click.argument("campaign_id", type=click.INT)
def list_teams(campaign_id):
    """List the team pages for a campaign"""
    teams = get_fundraising_teams_from_api(campaign_id)
    click.echo(f"Number of teams: {len(teams)}")
    if teams:
        click.secho("The following teams are in Classy:", fg="green")
        for team in teams:
            click.echo(f"[{team['id']}] {team['name']}")


@click.command()
@click.argument("campaign_id", type=click.INT)
def list_pages(campaign_id):
    """List the individual pages for a campaign"""
    pages = get_fundraising_pages_from_api(campaign_id)
    click.echo(f"Number of pages: {len(pages)}")
    if pages:
        click.secho("The following pages are in Classy:", fg="green")
        for page in pages:
            click.echo(f"[{page['id']}] {page['alias']}")


@click.command()
@click.argument("file_path", type=click.STRING)
@click.option(
    "--dry-run",
    "-d",
    is_flag=True,
    default=False,
    type=bool,
    show_default=True,
    help="Do a dry run instead of calling the Classy API",
)
def upload_transactions(file_path, dry_run):
    """Upload offline transactions through the Classy API"""
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
    errors = []
    for item in formatted:
        campaign_id = item["campaign_id"]
        transaction_payload = item["transaction"]
        dedication_payload = item["dedication"]

        if not dry_run:
            ok, transaction_result = create_offline_transaction(campaign_id, transaction_payload)
            if ok:
                transaction_id = transaction_result["id"]

                dedication_result = None
                if dedication_payload:
                    dedication_result = create_dedication(transaction_id, dedication_payload)

                # store the API results
                results[transaction_id] = {
                    "transaction": transaction_result,
                    "dedication": dedication_result,
                }
            else:
                errors.append({"paylod": transaction_payload, "result": transaction_result})

    right_now = datetime.now().strftime("%Y-%m-%d-%H:%M")

    if dry_run:
        # on dry runs, write the formatted input to a JSON file for inspection
        results = formatted
        log_file_path = f"output/dry-run-results-{right_now}.json"
    else:
        # on actual runs, write the responses from the API calls to a JSON file
        log_file_path = f"output/upload-results-{right_now}.json"

    with open(log_file_path, "w") as f:
        json.dump({"results": results, "errors": errors}, f, indent=2)

    click.secho(f"Done. Upload results logged to {log_file_path}", fg="green")
    if errors:
        click.secho(f"Errors encountered: {len(errors)}. Details in {log_file_path}", fg="red")


cli.add_command(list_campaigns)
cli.add_command(list_teams)
cli.add_command(list_pages)
cli.add_command(upload_transactions)


if __name__ == "__main__":
    cli()
